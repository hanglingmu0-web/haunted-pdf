# How the supplied PDFs work

English | [日本語](TECHNICAL.ja.md)

Inspected on October 21, 2026 (Japan Standard Time). Each file has one page and no Optional Content Groups (OCGs).

| File | Page size (pt) | Image XObjects | Widgets | Stamps | Active timer |
| --- | --- | ---: | ---: | ---: | --- |
| Snow_Night_Visitor.pdf | 512 × 768 | 42 | 41 | 0 | 600 ms |
| ningyo_halloween_pumpkin.pdf | 494 × 635 | 42 | 41 | 0 | 2000 ms |
| Ningyo_Halloween_Poster.pdf | 494 × 635 | 2 | 0 | 1 | None |

The number of image objects is not the number of distinct pictures. Deduplicating decoded image streams yields 34 distinct images in the movie poster and 41 in the animated doll.

## Animated demos

An initial image is painted into the page content. Above it are 41 full-page pushbutton Widgets. Each Widget's `/AP /N` appearance is a Form XObject containing an Image XObject for that frame. The image data is not stored as an ordinary field value in `/V`.

```text
Catalog
├─ Pages → one page → Contents → initial image
│                   └─ Annots → frame_01 ... frame_41
│                                 └─ AP / N → Form XObject → image
├─ AcroForm / Fields → the same 41 Widgets
├─ Names / JavaScript → document-level script with automatic startup
└─ OpenAction → ningyoStart();
```

Widgets use `/FT /Btn` and `/Ff 65536` (pushbutton). Their saved annotation flags, `/F 38`, combine Hidden (2), Print (4), and NoView (32). With Hidden set initially, they are also excluded from printing. During playback, the script switches `field.display` between `hidden` and `visible`. See [Adobe's Field.display reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/JS_API_AcroJS.html#display).

Each tick hides all Widgets and computes `step=(step+1)%48`. Steps 0 through 6 show only the page content; steps 7 through 47 show frame_01 through frame_41.

| Timing | Movie poster | Animated doll |
| --- | ---: | ---: |
| Tick interval | 0.6 seconds | 2 seconds |
| First Widget displayed | After 4.2 seconds | After 14 seconds |
| First Widget with pixels different from the initial image | frame_09: after 9 seconds | frame_02: after 16 seconds |
| Full cycle | 28.8 seconds | 96 seconds |

These are scheduled values from the code, not guarantees of real-time precision or smooth playback. Duplicate frames mean the picture does not change on every tick.

The startup function clears any existing timer before registering `app.setInterval()`. Both the document-level script and OpenAction invoke it. In the mock environment, only one timer remained active. See [Adobe's timer API](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/JS_API_AcroJS.html#setinterval).

Object 134 in the animated doll contains an unused older script. The current Names tree references object 137. Finding an old script through a text search alone does not establish the active behavior.

The animations do not fix a specific frame when printing. A field with `display.visible` may also print, so output depends on playback state and the viewer. This differs from the dedicated print-time demo below.

## Print-time demo

| Screen rendering | Print-mode rendering with annotations |
| --- | --- |
| ![Short hair](../previews/ningyo-print-screen.png) | ![Long hair](../previews/ningyo-print-output.png) |

Image A is painted into the page content. Image B is placed in the appearance of a Stamp annotation covering the same rectangle.

```text
/Subtype /Stamp
/Rect [0 0 494 635]
/F 36                 % Print 4 + NoView 32
/AP << /N ... >>      % Form XObject that paints image B
```

NoView suppresses the annotation on screen, while Print marks it for printing. Hidden is not set. Image A is not removed during printing: opaque image B covers the whole page. A transparent image or smaller annotation could leave A visible underneath. The flag values are also listed in [PDFium's definitions](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdf_annot.h).

Because these are not OCGs, they are not listed as layers in the layer panel. Annotation panels, attachment panels, or inspection tools can nevertheless reveal the structure or additional content. There is no guarantee that a viewer will not notice it.

When annotations are excluded from printing, B is omitted and A prints instead. This difference was verified using PDFium's print mode. See [Adobe's print settings documentation](https://helpx.adobe.com/acrobat/desktop/print-documents/use-secure-and-special-print-mode/print-comments.html).

## Chrome and other viewers

PDFium, used in Chromium-based viewers, includes a `setInterval` implementation. Its presence alone does not establish that these files play correctly in Chrome. JavaScript support, forms, annotation redraws, and host settings require testing in the actual application. PDFium rasterization in this repository is not a Chrome UI playback test. See the [PDFium implementation](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/fxjs/cjs_app.cpp).
