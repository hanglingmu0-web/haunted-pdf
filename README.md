# Haunted PDF: Animated Pictures and Print-Time Surprises

English | [日本語](README.ja.md)

Three single-page PDF demonstrations: a horror poster with an opening door, a Japanese doll whose hair grows, and a doll that looks different when printed. They use PDF forms, JavaScript, and annotations, without embedded videos, GIFs, or page-turn animation.

Repository: [hanglingmu0-web/haunted-pdf](https://github.com/hanglingmu0-web/haunted-pdf)

| Demo | PDF | How it works |
| --- | --- | --- |
| Snow Night Visitor | [Download](samples/Snow_Night_Visitor.pdf) | JavaScript switches between 41 image-backed buttons as the door opens |
| Growing-hair doll | [Download](samples/ningyo_halloween_pumpkin.pdf) | The same structure, with a slower animation |
| Print-time doll transformation | [Download](samples/Ningyo_Halloween_Poster.pdf) | Page content plus a print-only Stamp annotation; no JavaScript |

![Initial frame of Snow Night Visitor](previews/snow-start.jpg)

The preview above is a still image. Download the PDF to experience the effect. GitHub's preview is not a playback test. The supplied artwork retains its original Japanese text.

## Viewing the demos

The animations target the JavaScript environment in desktop Adobe Acrobat Reader. **Playback in Acrobat Reader and Chrome has not been tested for this repository.** Support and settings vary between viewers. When JavaScript does not run, the initial image remains available as ordinary page content.

The doll changes slowly. Its first button image appears after 14 seconds in the script's schedule, but that image duplicates the initial image. The first image with different pixels appears after 16 seconds. For the movie poster, these times are 4.2 seconds and 9 seconds, respectively. Actual timing depends on the viewer.

For the print-time demo, choose a print setting that includes stamps, such as **Document and Stamps** or **Document and Markups** in Acrobat. See the [screen/print comparison](docs/TECHNICAL.md#print-time-demo) and [Adobe's printing guidance](https://helpx.adobe.com/acrobat/desktop/print-documents/use-secure-and-special-print-mode/print-comments.html).

## Repository contents

- `samples/`: the three supplied PDFs, preserved byte for byte.
- `src/pdf_tools.py`: structure inspection, image extraction, PDF reconstruction, and comparison checks.
- `src/original/`: the active JavaScript extracted from each animation, for reference.
- `tests/timer.test.cjs`: frame order and timer checks using mocked Acrobat APIs.
- [Technical explanation](docs/TECHNICAL.md), [validation results](docs/VALIDATION.md), and [privacy inspection](docs/PRIVACY.md).
- [Review of the accompanying note article](docs/NOTE_REVIEW.md) and [publication information](docs/PUBLICATION.md).

The original artwork project and original production code were not supplied. The Python code in this repository reconstructs the PDF mechanisms using images extracted from the supplied PDFs. It does not regenerate the artwork from AI prompts.

## Reconstruct and validate

Requires Python 3.10 or later and Node.js. Run these commands from the repository root:

```sh
python -m venv .venv
# Activate the virtual environment before continuing.
python -m pip install -r requirements.txt
python src/pdf_tools.py inspect
python src/pdf_tools.py extract
python src/pdf_tools.py build
python src/pdf_tools.py validate
node tests/timer.test.cjs
```

Extracted assets go to `work/assets/`, reconstructed PDFs to `work/rebuilt/`, and validation outputs to `work/validation/`. The `work/` directory is excluded from Git.

Reconstructed PDFs are separate derivatives for comparing the images and mechanisms. Object numbers, compression, and metadata may differ. Original Content Credentials are not transplanted into these derivatives. The originals, including their provenance data, remain in `samples/`.

## Security limitations

Print-only content is neither encryption nor access control. It does not prevent printing, image extraction, or screenshots. These examples demonstrate visual effects, print-only notices, and document inspection; they are not a way to protect confidential data.

Static inspection of the supplied scripts found no external data submission, URL launching, local file retrieval, or external program execution. This finding applies to these three files and is not a general guarantee about PDF safety.

## Publication and usage terms

Published on October 21, 2026. No license has been specified for the PDFs, images, or code. The fictional movie poster is not an official production or announcement.
