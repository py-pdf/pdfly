# extract-text

Extract text from a PDF file.
## Usage

```
$ pdfly extract-text --help
 Usage: pdfly extract-text [OPTIONS] {pdf}

 Extract text from a PDF file.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf      <file>  [required]                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help        <bool>  Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the text from the 10th page of `document.pdf`, redirecting the output into `page.txt`.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf

```
