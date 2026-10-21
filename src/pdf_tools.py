"""Inspect, extract and reconstruct these three single-page PDF demonstrations.

No embedded PDF JavaScript is executed by this Python program.
Rebuilds are unsigned derivatives; original C2PA credentials remain in samples/.
"""
from pathlib import Path
from io import BytesIO
import argparse
import hashlib
import json
import re
from PIL import Image, ImageChops
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject,
    DictionaryObject, EncodedStreamObject, NameObject, NumberObject,
    TextStringObject, IndirectObject)

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    'snow': ('Snow_Night_Visitor.pdf', 600),
    'ningyo-animation': ('ningyo_halloween_pumpkin.pdf', 2000),
    'ningyo-print': ('Ningyo_Halloween_Poster.pdf', None),
}

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def objects(reader):
    seen = set()
    for gen, ids in reader.xref.items():
        for n in ids:
            if n and (n, gen) not in seen:
                seen.add((n, gen))
                yield n, reader.get_object(IndirectObject(n, gen, reader))
    for n in reader.xref_objStm:
        if (n, 0) not in seen:
            yield n, reader.get_object(n)

def js_text(action):
    value = action['/JS']
    return value.get_data().decode('utf-8') if hasattr(value, 'get_data') else str(value)

def active_script(reader):
    tree = reader.trailer['/Root']['/Names']['/JavaScript']
    # These samples have a single flat name tree, asserted rather than guessed.
    names = tree['/Names']
    assert len(names) == 2
    return js_text(names[1].get_object())

def only_image(resources):
    values = [x.get_object() for x in resources['/XObject'].values()]
    assert len(values) == 1 and values[0]['/Subtype'] == '/Image'
    return values[0]

def ordered_images(reader):
    page = reader.pages[0]
    yield only_image(page['/Resources'])
    for ref in page['/Annots']:
        yield only_image(ref.get_object()['/AP']['/N']['/Resources'])

def image_pil(obj):
    data = obj.get_data()
    if '/DCTDecode' in str(obj.get('/Filter')):
        return Image.open(BytesIO(data)).convert('RGB')
    assert obj['/ColorSpace'] == '/DeviceRGB' and obj['/BitsPerComponent'] == 8
    return Image.frombytes('RGB', (int(obj['/Width']), int(obj['/Height'])), data)

def inspect(path):
    reader = PdfReader(path)
    root = reader.trailer['/Root']
    all_objects = list(objects(reader))
    images = [o for _, o in all_objects if isinstance(o, dict) and o.get('/Subtype') == '/Image']
    scripts = [{'object': n, 'code': js_text(o)} for n, o in all_objects
               if isinstance(o, dict) and '/JS' in o]
    annotations = [{key: str(ref.get_object().get(key, ''))
                    for key in ['/Subtype', '/T', '/F', '/Ff', '/Rect']}
                   for page in reader.pages for ref in page.get('/Annots', [])]
    return {
        'file': path.name, 'bytes': path.stat().st_size,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'pages': len(reader.pages), 'page_size': list(reader.pages[0].mediabox),
        'image_objects': len(images),
        'unique_decoded_image_streams': len({hashlib.sha256(o.get_data()).hexdigest() for o in images}),
        'fields': len(reader.get_fields() or {}), 'annotations': annotations,
        'ocg': '/OCProperties' in root, 'metadata': dict(reader.metadata or {}),
        'embedded_files': [{'name': name, 'bytes': [len(b) for b in blobs]}
                           for name, blobs in reader.attachments.items()],
        'eof_markers': path.read_bytes().count(b'%%EOF'),
        'scripts': scripts,
    }

def extract():
    for key, (filename, interval) in SAMPLES.items():
        reader = PdfReader(ROOT/'samples'/filename)
        out = ROOT/'work/assets'/key
        out.mkdir(parents=True, exist_ok=True)
        files = []
        for i, obj in enumerate(ordered_images(reader)):
            extension = '.jpg' if '/DCTDecode' in str(obj.get('/Filter')) else '.png'
            filename_out = f'{i:02d}{extension}'
            if extension == '.jpg':
                (out/filename_out).write_bytes(obj.get_data())
            else:
                image_pil(obj).save(out/filename_out)
            files.append(filename_out)
        manifest = {'kind': 'animation' if interval else 'print',
                    'width': float(reader.pages[0].mediabox.width),
                    'height': float(reader.pages[0].mediabox.height),
                    'interval_ms': interval, 'images': files, 'source': filename}
        dump(out/'manifest.json', manifest)
        if interval:
            (out/'animation.js').write_text(active_script(reader), encoding='utf-8')
        print(f'Extracted {key}: {len(files)} image objects')

def dic(**kwargs):
    return DictionaryObject({NameObject('/'+k): v for k, v in kwargs.items()})

def nums(values):
    from pypdf.generic import FloatObject
    return ArrayObject([FloatObject(x) for x in values])

def image_object(writer, path):
    im = Image.open(path).convert('RGB')
    if path.suffix.lower() in ('.jpg', '.jpeg'):
        stream = EncodedStreamObject()
        stream._data = path.read_bytes()
        stream[NameObject('/Filter')] = NameObject('/DCTDecode')
    else:
        stream = DecodedStreamObject()
        stream.set_data(im.tobytes())
        stream = stream.flate_encode()
    stream.update(dic(Type=NameObject('/XObject'), Subtype=NameObject('/Image'),
                      Width=NumberObject(im.width), Height=NumberObject(im.height),
                      ColorSpace=NameObject('/DeviceRGB'), BitsPerComponent=NumberObject(8)))
    return writer._add_object(stream)

def paint_stream(width, height):
    stream = DecodedStreamObject()
    stream.set_data(f'q\n{width:g} 0 0 {height:g} 0 0 cm\n/Im0 Do\nQ\n'.encode('ascii'))
    return stream

def resources(image):
    return dic(XObject=dic(Im0=image))

def build():
    for key, (_, interval) in SAMPLES.items():
        folder = ROOT/'work/assets'/key
        m = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        writer = PdfWriter()
        w, h = m['width'], m['height']
        page = writer.add_blank_page(width=w, height=h)
        images = [image_object(writer, folder/f) for f in m['images']]
        page[NameObject('/Resources')] = resources(images[0])
        page[NameObject('/Contents')] = writer._add_object(paint_stream(w, h))
        refs = ArrayObject()
        for i, img in enumerate(images[1:], 1):
            ap = paint_stream(w, h)
            ap.update(dic(Type=NameObject('/XObject'), Subtype=NameObject('/Form'),
                          FormType=NumberObject(1), BBox=nums([0, 0, w, h]), Resources=resources(img)))
            annot = dic(Type=NameObject('/Annot'),
                        Subtype=NameObject('/Widget' if interval else '/Stamp'),
                        Rect=nums([0, 0, w, h]), F=NumberObject(38 if interval else 36),
                        AP=dic(N=writer._add_object(ap)), P=page.indirect_reference)
            if interval:
                annot.update(dic(FT=NameObject('/Btn'), Ff=NumberObject(65536),
                                 T=TextStringObject(f'frame_{i:02d}'),
                                 H=NameObject('/N'), BS=dic(W=NumberObject(0))))
            refs.append(writer._add_object(annot))
        page[NameObject('/Annots')] = refs
        if interval:
            assert len(refs) == 41
            writer._root_object[NameObject('/AcroForm')] = writer._add_object(
                dic(Fields=refs, NeedAppearances=BooleanObject(False)))
            # This copies the inspected active script, preserving the original timing.
            main = (folder/'animation.js').read_text(encoding='utf-8')
            action = writer._add_object(dic(S=NameObject('/JavaScript'), JS=TextStringObject(main)))
            writer._root_object[NameObject('/Names')] = dic(JavaScript=dic(
                Names=ArrayObject([TextStringObject('animation'), action])))
            writer._root_object[NameObject('/OpenAction')] = writer._add_object(
                dic(S=NameObject('/JavaScript'), JS=TextStringObject('ningyoStart();')))
        writer.add_metadata({'/Title': key+' (reconstructed)',
                             '/Subject': 'Unsigned reconstruction; original provenance is in samples/'})
        dest = ROOT/'work/rebuilt'/f'{key}.pdf'
        dest.parent.mkdir(parents=True, exist_ok=True)
        writer.write(dest)
        print(f'Built {dest.name}')

def render(path, output, printing=False, annots=True):
    import pypdfium2 as pdfium
    with pdfium.PdfDocument(path) as doc:
        page = doc[0]
        bitmap = page.render(scale=1.5, draw_annots=annots, may_draw_forms=False,
                             optimize_mode='print' if printing else None)
        im = bitmap.to_pil().convert('RGB')
        output.parent.mkdir(parents=True, exist_ok=True)
        im.save(output)
        bitmap.close(); page.close()
        return im

def validate():
    results = []
    for key, (filename, interval) in SAMPLES.items():
        source = ROOT/'samples'/filename
        rebuilt = ROOT/'work/rebuilt'/f'{key}.pdf'
        a, b = PdfReader(source), PdfReader(rebuilt)
        assert len(a.pages) == len(b.pages) == 1
        ai, bi = list(ordered_images(a)), list(ordered_images(b))
        assert len(ai) == len(bi) == (42 if interval else 2)
        for old, new in zip(ai, bi):
            assert image_pil(old).tobytes() == image_pil(new).tobytes()
        for r in (a, b):
            assert '/OCProperties' not in r.trailer['/Root']
            annotations = r.pages[0]['/Annots']
            assert len(annotations) == (41 if interval else 1)
            width, height = float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)
            for ref in annotations:
                annot = ref.get_object()
                assert list(annot['/Rect']) == [0, 0, width, height]
                ap = annot['/AP']['/N']
                assert ap['/Subtype'] == '/Form'
                assert list(ap['/BBox']) == [0, 0, width, height]
                assert ap.get_data().strip()
            if interval:
                fields = r.trailer['/Root']['/AcroForm']['/Fields']
                assert [(x.idnum, x.generation) for x in fields] == [(x.idnum, x.generation) for x in annotations]
                assert set(r.get_fields()) == {f'frame_{i:02d}' for i in range(1, 42)}
                assert all(ref.get_object()['/F'] == 38 for ref in annotations)
                assert all(ref.get_object()['/Ff'] == 65536 and ref.get_object()['/FT'] == '/Btn'
                           for ref in annotations)
                assert active_script(r) == active_script(a)
                assert js_text(r.trailer['/Root']['/OpenAction']) == 'ningyoStart();'
            else:
                assert not r.get_fields()
                assert annotations[0].get_object()['/Subtype'] == '/Stamp'
                assert annotations[0].get_object()['/F'] == 36
                assert not any('/JS' in o for _, o in objects(r) if isinstance(o, dict))
        out = ROOT/'work/validation'
        screen = render(source, out/f'{key}-screen.png')
        rebuilt_screen = render(rebuilt, out/f'{key}-rebuilt-screen.png')
        assert ImageChops.difference(screen, rebuilt_screen).getbbox() is None
        record = {'sample': filename, 'structure': 'pass', 'all_image_pixels_preserved': True,
                  'screen_render_matches': True}
        if not interval:
            printed = render(source, out/f'{key}-print.png', printing=True)
            rebuilt_printed = render(rebuilt, out/f'{key}-rebuilt-print.png', printing=True)
            no_annots = render(source, out/f'{key}-print-without-annotations.png', printing=True, annots=False)
            assert ImageChops.difference(printed, rebuilt_printed).getbbox() is None
            assert ImageChops.difference(screen, printed).getbbox() is not None
            assert ImageChops.difference(screen, no_annots).getbbox() is None
            record.update(print_render_matches=True, screen_differs_from_print=True,
                          omitting_annotations_returns_screen_image=True)
        else:
            dump(out/f'{key}-js.json', {'main':active_script(a),
                 'open':js_text(a.trailer['/Root']['/OpenAction']), 'interval':interval})
        results.append(record)
    dump(ROOT/'work/validation/results.json', results)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['inspect', 'extract', 'build', 'validate'])
    args = parser.parse_args()
    if args.command == 'inspect':
        for key, (filename, _) in SAMPLES.items():
            dump(ROOT/'work/inspection'/f'{key}.json', inspect(ROOT/'samples'/filename))
    else:
        {'extract':extract, 'build':build, 'validate':validate}[args.command]()
