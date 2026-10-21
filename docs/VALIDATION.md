# Validation results

English | [日本語](VALIDATION.ja.md)

Validated on Windows on October 21, 2026 (Japan Standard Time).

Environment: pypdf 6.10.0, Pillow 12.3.0, pypdfium2 5.14.0, and PDFium 156.0.8076.0. Poppler 26.07.0 was also used for initial visual inspection.

After publication, [GitHub Actions passed](https://github.com/hanglingmu0-web/haunted-pdf/actions/runs/39586157385) on October 21, 2026 for commit `4ba30eb56a9e544bfbab33b24d18a547f023db47`. The Ubuntu runner checked original hashes, extraction, reconstruction, image comparisons, and mocked timers. All three published PDFs were also downloaded without authentication and matched the originals' SHA-256 hashes.

## Completed checks

| Check | Result |
| --- | --- |
| Page counts, image counts, annotation types, and absence of OCGs | Passed for all three files |
| The 41 fields and 41 page Widgets reference the same objects | Passed for both animations |
| Names, rectangles, initial flags, nonempty normal appearances, and image order | Checked |
| Identification of active scripts through Names and OpenAction | Completed |
| Decoded RGB pixels of all 86 images preserved during reconstruction | Passed |
| Original/reconstructed initial screen renders match exactly | Passed for all three files |
| Print-time Stamp uses `/F 36`, with no AcroForm or JavaScript | Passed |
| Print-time demo differs between screen and print modes | Passed |
| Excluding annotations returns the screen image in print mode | Passed |
| Original/reconstructed print-mode renders match | Passed |
| Each animation's JavaScript executed for 144 ticks (three cycles) with mocked Acrobat APIs | Passed |
| Automatic startup, prevention of duplicate timers, frame order, return to initial display | Passed in mock environment |
| Supplied originals and published copies have identical SHA-256 hashes | Passed for all three files |

`validate` compares page/image/field structure, all image pixels, and PDFium renders. `timer.test.cjs` runs the extracted active scripts and checks which fields are visible on every tick, rather than only testing a separate new implementation.

PDFium used `draw_annots=True` and `optimize_mode='print'` to enable its print rendering flag. The print result was not simulated by manually compositing image B. However, it was a rasterization test, not a physical print test. Screen comparisons for the animations cover the initial still image, not animated form rendering in a viewer.

## Not tested

- Actual Adobe Acrobat Reader playback, version differences, and redraw smoothness.
- Actual playback or printing in Chrome, Edge, Firefox, macOS Preview, or mobile viewers.
- Physical printers, printer drivers, and Acrobat's print dialog.
- Printing either animation while it is playing.
- C2PA signature trust, validity, and binding to the original data.

## Manual viewer test procedure

1. Record the operating system and viewer version.
2. Open the movie poster and observe changes after approximately 9 seconds and a cycle of approximately 28.8 seconds.
3. Open the animated doll and observe changes after approximately 16 seconds and a cycle of approximately 96 seconds. Watch for more than two minutes because the animation is slow.
4. Open the print-time demo and confirm that it shows short hair on screen.
5. Compare print preview and output with stamps included and excluded: expect long hair when included and short hair when excluded.
6. Add measured results and the environment to this document. Keep untested environments explicitly marked as untested.

Structural checks alone must not be described as successful Acrobat or Chrome playback tests.
