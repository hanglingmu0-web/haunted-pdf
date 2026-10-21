from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import IndirectObject, TextStringObject, ByteStringObject
from PIL import Image
from io import BytesIO
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'work/audit'
OUT.mkdir(parents=True,exist_ok=True)
FILES=['Snow_Night_Visitor.pdf','ningyo_halloween_pumpkin.pdf','Ningyo_Halloween_Poster.pdf']
def objects(r):
    seen=set()
    for gen,ids in r.xref.items():
        for n in ids:
            if n and (n,gen) not in seen:
                seen.add((n,gen)); yield n,r.get_object(IndirectObject(n,gen,r))
    for n in r.xref_objStm:
        if (n,0) not in seen: yield n,r.get_object(n)

def strings(obj,path='',depth=0):
    if depth>20:return
    if isinstance(obj,IndirectObject):return
    if isinstance(obj,(TextStringObject,ByteStringObject)):
        yield {'path':path,'value':str(obj)}
    elif isinstance(obj,dict):
        for k,v in obj.items():yield from strings(v,path+'/'+str(k),depth+1)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):yield from strings(v,path+f'[{i}]',depth+1)

for filename in FILES:
    p=ROOT/'samples'/filename
    data=p.read_bytes(); r=PdfReader(p)
    dest=OUT/p.stem;dest.mkdir(exist_ok=True)
    report={'file':filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
       'metadata':dict(r.metadata or {}),'catalog_keys':list(r.trailer['/Root']),
       'eof_markers':data.count(b'%%EOF'),'strings':[],'streams':[], 'images':[], 'attachments':[], 'actions':[]}
    allstrings=[]
    for n,obj in objects(r):
        report['strings'].extend(strings(obj,f'obj{n}'))
        if not isinstance(obj,dict):continue
        if '/S' in obj:report['actions'].append({'object':n,'type':str(obj['/S'])})
        if obj.get('/Subtype')=='/Image':
            b=obj.get_data()
            if '/DCTDecode' in str(obj.get('/Filter')):im=Image.open(BytesIO(b))
            else:
                mode={'/DeviceRGB':'RGB','/DeviceGray':'L','/DeviceCMYK':'CMYK'}[str(obj['/ColorSpace'])]
                im=Image.frombytes(mode,(int(obj['/Width']),int(obj['/Height'])),b)
            exif={str(k):str(v) for k,v in im.getexif().items()}
            info={k:str(v)[:2000] for k,v in im.info.items()}
            report['images'].append({'object':n,'size':im.size,'exif':exif,'info':info,'decoded_sha256':hashlib.sha256(b).hexdigest()})
            im.convert('RGB').save(dest/f'image-{n:03d}.png')
            # Search JPEG metadata, not arbitrary raw RGB pixels.
            if '/DCTDecode' in str(obj.get('/Filter')):allstrings += re.findall(rb'[ -~]{6,}',b)
        elif hasattr(obj,'get_data'):
            b=obj.get_data(); allstrings += re.findall(rb'[ -~]{6,}',b)
            if obj.get('/Type')=='/EmbeddedFile':
                (dest/f'attachment-{n}.bin').write_bytes(b)
                readable=[x.decode('ascii') for x in re.findall(rb'[ -~]{4,}',b)]
                (dest/f'attachment-{n}-strings.json').write_text(json.dumps(readable,ensure_ascii=False,indent=2),encoding='utf-8')
                report['attachments'].append({'object':n,'bytes':len(b),'subtype':str(obj.get('/Subtype')),'readable_strings':readable})
            else:
                report['streams'].append({'object':n,'bytes':len(b),'text':b.decode('utf-8',errors='replace')[:20000]})
    allstrings += re.findall(rb'[ -~]{6,}',data)
    joined='\n'.join(s.decode('ascii',errors='replace') for s in allstrings)+'\n'+json.dumps(report['strings'],ensure_ascii=False)
    pats={'email':r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',
          'windows_user_path':r'[A-Za-z]:[\\/](?:Users|Documents and Settings)[^\n<>\"\x00]{0,150}',
          'unix_home':r'/(?:Users|home)/[^\s<>\"\x00]{1,150}',
          'url':r'https?://[^\s<>\"\x00]{3,200}',
          'phone_candidate':r'(?<!\d)(?:\+81[- ]?|0)(?:\d[- ]?){8,10}(?!\d)'}
    report['pattern_candidates']={k:sorted(set(re.findall(v,joined)))[:100] for k,v in pats.items()}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['file','bytes','sha256','metadata','eof_markers','pattern_candidates','actions']},ensure_ascii=False))
    print('images',len(report['images']),'image metadata',[(x['object'],x['exif'],x['info']) for x in report['images'] if x['exif'] or x['info']])
    print('text strings',report['strings'])
    print('attachments',[(a['object'],a['bytes'],a['subtype']) for a in report['attachments']])
    # Every image in source object order, labelled with object ID.
    from PIL import ImageDraw
    thumbs=report['images']; cellw,cellh=180,260
    sheet=Image.new('RGB',(cellw*7,cellh*((len(thumbs)+6)//7)),(242,242,242));d=ImageDraw.Draw(sheet)
    for i,entry in enumerate(thumbs):
        im=Image.open(dest/f"image-{entry['object']:03d}.png");im.thumbnail((174,232))
        x=(i%7)*cellw;y=(i//7)*cellh
        sheet.paste(im,(x+(cellw-im.width)//2,y+22));d.text((x+6,y+4),f"obj {entry['object']}",fill='black')
    sheet.save(dest/'contact-sheet.jpg')
