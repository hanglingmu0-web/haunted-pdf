# Publication information

English | [日本語](PUBLICATION.ja.md)

Repository: [hanglingmu0-web/haunted-pdf](https://github.com/hanglingmu0-web/haunted-pdf)

Published on October 21, 2026 (Japan Standard Time). The public branch is `main`. English is the default documentation language; Japanese versions are linked from each document.

## Links for the accompanying article

- [Repository and documentation](https://github.com/hanglingmu0-web/haunted-pdf)
- [Movie-poster PDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/Snow_Night_Visitor.pdf)
- [Animated-doll PDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/ningyo_halloween_pumpkin.pdf)
- [Print-time transformation PDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/Ningyo_Halloween_Poster.pdf)
- [Validation results](VALIDATION.md)
- [Privacy inspection](PRIVACY.md)
- [Japanese documentation](../README.ja.md)

Open the PDF's page, download the file, and use a supporting viewer. These links do not imply that the animation plays in GitHub's preview.

## Published content

The repository contains the three supplied original PDFs, preview images, reconstruction and inspection code, validation results, technical documentation, and a review of the proposed note article. The original PDFs total 46,265,955 bytes. Their SHA-256 hashes are recorded in `SHA256SUMS.txt`.

Working logs, workstation paths, virtual environments, and extracted intermediate images are excluded. Commits use a GitHub noreply email address.

## Verify the originals

```sh
python src/verify_hashes.py
```

See the [README](../README.md) for reconstruction commands and [validation report](VALIDATION.md) for manual viewer checks. GitHub Actions checks image equality, structure, and mocked timers; it does not test Acrobat or Chrome applications.

## Usage terms and validation scope

No license has been specified. The fictional movie poster is not an official production or announcement. Checking PDFs for personal information is separate from checking rights to source artwork. Actual viewer results should be added with environment and version information after testing.
