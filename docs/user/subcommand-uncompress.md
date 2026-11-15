# uncompress

Uncompress the page content streams of a PDF.

## Usage

```
$ pdfly uncompress --help
 Usage: pdfly uncompress [OPTIONS] {pdf} {output}

 Uncompress the page content streams of a PDF.

 This makes the drawing operators of every page human-readable, e.g. for
 debugging. Fonts, images and other streams are not uncompressed.

 Example:
     pdfly uncompress input.pdf output.pdf

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf         <file>  [required]                                          │
│ *    output      <path>  [required]                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help        <bool>  Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

Uncompress the page content streams of `document_compressed.pdf` and write the
output to `document.pdf`:

```
pdfly uncompress document_compressed.pdf document.pdf
```
