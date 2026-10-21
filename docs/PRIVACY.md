# Privacy inspection before publication

English | [日本語](PRIVACY.ja.md)

Inspected on October 21, 2026 (Japan Standard Time). The scope was the three files in `samples/`; their SHA-256 hashes are recorded in `SHA256SUMS.txt`.

**Within the inspected scope, no personal name, email address, home address, phone number, computer username, or local storage path belonging to the user was identified. The PDFs were not modified to remove personal information.**

| File | Personal information identified | Other retained information |
| --- | --- | --- |
| Snow_Night_Visitor.pdf | None identified | Title/Subject/Creator describing the work and production method; a UUID in the JavaScript name tree |
| ningyo_halloween_pumpkin.pdf | None identified | Producer; Content Credentials (24,296 bytes); an unused older script |
| Ningyo_Halloween_Poster.pdf | None identified | Generic artwork title and Creator; Content Credentials (24,296 bytes); a previous incremental-save revision |

## Inspection scope

- Info dictionaries, Catalog entries, presence of XMP, PDF strings, and name trees.
- Text from all pages, all 86 Image XObjects, image/JPEG metadata, and presence of EXIF/GPS data.
- Contact sheets covering all 42 images in each animation, enlarged initial/final movie-poster images, and the doll's screen/print images.
- AcroForm, every Widget/Stamp annotation, Actions, currently referenced JavaScript, and unused older JavaScript.
- Embedded files registered under `/AF` and `/EmbeddedFiles`.
- JUMBF/CBOR data in Content Credentials and the subject, issuer, and extensions of embedded X.509 certificates.
- The print-time PDF's previous incremental-save revision: its Info and Catalog were read, and objects 1 through 9 were confirmed to remain in the current structure.
- Email-, path-, URL-, and phone-like strings in raw PDF bytes and decoded streams, with contextual review of automated matches.

Extracted page text was empty in all three PDFs, so text within images was reviewed visually. No EXIF/GPS data was detected. Additional JPEG information consisted of ordinary JFIF fields such as density. No image text identified as an address or contact detail was found.

Two short email-like matches occurred within random compressed-image bytes, rather than PDF string values or image metadata. Many phone-like candidates were ten-digit offsets in xref tables. These were not counted as contact information.

## Content Credentials

Both doll PDFs carry provenance records. Decoded data included:

- Generator name: ChatGPT.
- Recorded `softwareAgent` name and version: `gpt-6-thinking`.
- Recorded creation times: approximately October 16, 2026, 09:59:24 for the animation and October 20, 2026, 09:37:14 for the print-time demo, both converted to Japan Standard Time (UTC+09:00).
- Per-work manifest and instance IDs, hashes, signatures, and timestamp information.
- Organizational certificates for OpenAI and SSL Corporation, plus certificate lookup URLs.

These are values found in the records. The creation times do not necessarily describe completion of the final PDFs. C2PA signature validity and binding to these PDFs were not verified.

The certificates contain US organization names and locations, rather than the user's personal name or home address. The certificate usage label `emailProtection` is not itself an email address. No user email address, prompt, conversation text, or account name was identified.

Creation times and artwork IDs may help correlate a file with another copy or production record. Absence of a personal name does not mean absence of provenance. The originals' Content Credentials were retained.

## Scripts and external references

The inspected scripts control frame visibility, timers, and error messages. No data submission, external URL launching, file retrieval, or external program execution code was identified. URLs within certificates refer to certificate or revocation information; they are not submission destinations in the animation scripts. Any network activity performed by a viewer itself, such as certificate verification, is outside this static inspection.

## Limitations

This was a routine pre-publication inspection. It did not include OCR of every image, steganalysis, cryptographic certificate validation, identification of people from faces, or correlation with external datasets. It does not mathematically guarantee the absence of undiscovered personal information. The identity of people depicted and rights to source artwork were not determined by this inspection.

Published copies have the same SHA-256 hashes as the originals. Inspection workstation paths, computer usernames, and detailed working logs are not included in the publication package.

## Repeat the inspection

```sh
python -m pip install -r requirements-audit.txt
python src/audit_privacy.py
python src/inspect_credentials.py
```

Results are written to `work/audit/`. Regular-expression matches are candidates requiring contextual and visual review, not confirmed findings. The tools extract attachments and images; do not publish their working logs without review when adapting them to other PDFs. The credentials parser supports the CBOR structures encountered in these two samples and is not a general C2PA validator. A failure on an unknown format means further analysis is needed, not that no information exists.
