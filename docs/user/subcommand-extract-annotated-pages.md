# extract-annotated-pages

Extract only the annotated pages from a PDF. This can help to review or rework pages from a large document iteratively.

## Usage

```
pdfly extract-annotated-pages --help

 Usage: pdfly extract-annotated-pages [OPTIONS] INPUT_PDF

 Extract only the annotated pages from a PDF.

 Q: Why does this help?
 A: https://github.com/py-pdf/pdfly/issues/97

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input_pdf      FILE  Input PDF file. [required]                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      PATH  Output PDF file. Defaults to 'input_pdf_annotated'.                                                      │
│ --help                  Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Examples

### Input file

Extracts only pages containing annotations from a file `input.pdf`. Pages are written into a new file `input_annotated.pdf`.

```
pdfly extract-annotated-pages input.pdf
```

### Input file with specific output file

Extracts only pages containing annotations from a file `input.pdf` into the given output file `pages_to_rework.pdf`.


```
pdfly extract-annotated-pages input.pdf -o pages_to_rework.pdf
```
