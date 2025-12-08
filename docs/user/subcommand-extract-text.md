# extract-text

Extract text from a PDF file.
## Usage

```
$ pdfly extract-text --help
 Usage: pdfly extract-text [OPTIONS] PDF

 Extract text from a PDF file. Supports selecting a range.


╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf      FILE  [default: None] [required]                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --from INTEGER   Inclusive starting page index (0-based).                    │
│ --end INTEGER    Inclusive ending page index (0-based).                      │
│ --help           Show this message and exit.                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the text from the 10th page of `document.pdf`, redirecting the output into `page.txt`.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf

Extract text for a specific range of pages directly:

```
pdfly extract-text document.pdf --from 0 --end 0   # only first page
pdfly extract-text document.pdf --from 2            # pages from index 2 to end
pdfly extract-text document.pdf --end 5             # pages from start to index 5
```

```
