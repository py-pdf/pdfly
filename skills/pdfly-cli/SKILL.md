---
name: pdfly-cli
description: |
  A pure-python CLI application for manipulating PDF files. Use when needing to compress, merge, split, rotate, sign, extract images/text, or convert files to/from PDF. Commands: 2-up, booklet, cat, check-sign, compress, extract-annotated-pages, extract-images, extract-text, meta, pagemeta, rm, rotate, sign, uncompress, update-offsets, x2pdf. Trigger phrases: "compress PDF", "merge PDFs", "split PDF", "rotate pages", "extract images from PDF", "sign PDF", "PDF metadata", "convert to PDF".
---

# pdfly CLI Skill

A pure-python CLI for PDF manipulation built on [pypdf](https://pypdf.readthedocs.io/), [fpdf2](https://pyfpdf.github.io/fpdf2/), and [endesive](https://endesive.readthedocs.io/).

## Installation

```bash
pip install pdfly
# or with uv
uvx pdfly --help
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `pdfly compress IN OUT` | Lossless compression |
| `pdfly cat IN [PAGES]... -o OUT` | Merge/split pages |
| `pdfly rm IN [PAGES]... -o OUT` | Remove pages |
| `pdfly rotate -o OUT IN DEG [PGRGS]` | Rotate pages |
| `pdfly sign IN --p12 CERT [-o OUT]` | Sign PDF |
| `pdfly check-sign IN --pem CERT` | Verify signature |
| `pdfly meta IN [-o FORMAT]` | Show metadata |
| `pdfly pagemeta IN IDX [-o FORMAT]` | Page details (0-based) |
| `pdfly extract-images IN` | Extract images |
| `pdfly extract-text IN` | Extract text |
| `pdfly extract-annotated-pages IN [-o OUT]` | Extract annotated |
| `pdfly uncompress IN OUT` | Decompress streams |
| `pdfly update-offsets IN [-o OUT]` | Fix offsets |
| `pdfly 2-up IN OUT` | 2-up layout |
| `pdfly booklet IN OUT [-b FILE] [-c FILE]` | Booklet layout |
| `pdfly x2pdf [FILES]... -o OUT` | Convert to PDF |

## Output Formats (meta/pagemeta)

```bash
-o text   # Default
-o json
-o yaml
```

## Page Range Syntax

See [references/page-ranges.md](references/page-ranges.md) for full syntax including negative indices and strides.

## PDF Signing

See [references/sign.md](references/sign.md) for complete signing/verification workflow.

## Rotate Command

The `-o/--output` option is **required** and must come **before** positional arguments:

```bash
pdfly rotate -o output.pdf input.pdf 90 "1-3"
```

See [references/rotate.md](references/rotate.md) for full examples.

## Extract/Merge (cat)

See [references/cat.md](references/cat.md) for complex merge/split operations.

## Key Libraries

| Library | Purpose |
|---------|---------|
| `pypdf` | PDF reading/writing, page manipulation |
| `fpdf2` | Creating PDFs from images/text |
| `endesive` | PDF signing with PKCS12 |
| `pillow` | Image processing |
| `cryptography` | Cryptographic operations |

## Exit Codes

- `0` = Success
- `1` = Error (file not found, invalid input, etc.)
