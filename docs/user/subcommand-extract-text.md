# extract-text

Extract text from a PDF file.
## Usage

```
$ pdfly extract-text --help
 Usage: pdfly extract-text [OPTIONS] PDF

 Extract text from a PDF file.

 Offers an option to store the whole output in a single file, or each page's text in a different file,
 allowing custom naming patterns for the output files.

┌─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ *    pdf      FILE  [required]                                                                                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ --output-pattern  -o      TEXT  Naming pattern for output files. If none is entered, output is echoed. If it contains │
│                                 "[]" substrings, each page's text is output in a different file and the "[]"          │
│                                 substrings in the filename are replaced by the page's index. If there are no "[]"     │
│                                 substrings, the output is stored in one file.                                         │
│ --help                          Show this message and exit.                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## Examples

Extract the text from the 10th page of `document.pdf`.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf

```

Extract the text from `document.pdf` and store each page's text in a file called `page-X.txt`, where X is the index of the page.

```
pdfly extract-text document.pdf -o page-[].txt

```
