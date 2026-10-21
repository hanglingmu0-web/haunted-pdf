# Review of the accompanying note article

English | [日本語](NOTE_REVIEW.ja.md)

The three supplied files cover all three demonstrations in the proposed Japanese note article. The suggestions below reflect inspection of those files. This document translates the editorial guidance; the Japanese version contains replacement wording for the original article.

## 1. Introduction and publication link

Correct the introduction's grammatical error and use the following meaning:

> The technical explanation and reconstruction code are available on [GitHub](https://github.com/hanglingmu0-web/haunted-pdf), together with the validation results.

## 2. Viewer compatibility

The wording that lists Acrobat Reader and Chrome as JavaScript-capable viewers could imply uniform compatibility. Replace it with:

> The animations target desktop Adobe Acrobat Reader's JavaScript environment. They may not work in some viewers, including browser-based viewers, depending on feature support and settings. Tested and untested environments are listed separately in the GitHub validation report.

The completed checks cover structural analysis, mocked JavaScript execution, and PDFium rendering. Do not claim actual Acrobat or Chrome playback has been tested.

## 3. Explain frame storage precisely

> One initial image is painted into the page. Forty-one images are overlaid as AcroForm button appearances. JavaScript switches the buttons between visible and hidden states. The single page contains 42 image objects, some with identical content.

“Stored in AcroForm fields” is a useful overview, but the images are specifically Image XObjects within Widget appearances.

The initial pause may make readers think the animation has failed. Near the doll PDF link, mention that the first changed image appears after about 16 seconds and a full cycle takes about 96 seconds. Actual timing depends on the viewer.

## 4. Distinguish layers from Stamp annotations

Immediately after the article introduces layer-based display and print settings, clarify:

> PDF provides several ways to vary screen and print output. Layer settings are one option, but this doll uses a Stamp annotation that appears only when printing, rather than PDF layers.

Consolidate the repeated explanation that the implementation does not use OCGs:

> The short-haired image A is painted into the page, and the long-haired image B is overlaid as a Stamp annotation. With Print and NoView set, a supporting viewer shows A on screen and B when annotations are included in printing. B covers A from above.

## 5. Qualify claims that hidden content cannot be noticed

Replace categorical wording with:

> Someone looking only at the page may not notice the additional image. Annotation lists and inspection tools can reveal it, so this is not a secrecy mechanism.

## 6. Frame the security discussion around inspection

The original caveats about encryption and access control are appropriate. To avoid recommending concealment as protection, change the heading about hiding real data behind a dummy image to “Information that is not displayed can still remain inside a PDF.”

> This is an example of why looking at the screen is not a complete inspection of a PDF. Print-only notices can be useful, but this mechanism should not be used to conceal confidential data for distribution. The undisplayed images remain in the file and can be extracted.

If the analogy of hiding something behind a picture frame is retained, connect it to document design and inspection. In these samples, provenance data and an unused script were also present without being part of the visible page.

## 7. Historical claims about attacks

The claim that PDF JavaScript has been a breeding ground for zero-day attacks or malware requires specific primary-source support if retained. That historical claim was not verified in this project. A concise alternative is:

> PDF JavaScript may be restricted by viewer or organizational settings. These examples will not work in every environment.

## 8. Improve instructions to an AI agent

Add the following to the article's existing verification checklist:

> Identify active JavaScript by following Names and OpenAction references, not just searching text. Confirm that AcroForm Fields and page Widgets reference the same objects. Distinguish originals, reconstructed PDFs, and image assets. Inspect personal information and provenance data such as Content Credentials. Explicitly mark anything not tested in an actual viewer as untested.

## Article asset mapping

| Article illustration or link | Repository asset |
| --- | --- |
| Initial animated-doll image | `previews/ningyo-animation-start.png` |
| Animated-doll PDF | `samples/ningyo_halloween_pumpkin.pdf` |
| Movie poster with closed door | `previews/snow-start.jpg` |
| Animated movie-poster PDF | `samples/Snow_Night_Visitor.pdf` |
| Print-time demo's screen image | `previews/ningyo-print-screen.png` |
| Illustration of print output | `previews/ningyo-print-output.png` |
| Print-time transformation PDF | `samples/Ningyo_Halloween_Poster.pdf` |

Label the print-output illustration as a PDFium print-mode render, not a photograph of a physical print. The animated and print-time dolls have different details, including their pumpkin decorations; use the matching assets for each example.
