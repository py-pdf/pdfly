# meta

Extract text from a PDF file.
## Usage

```
$ pdfly extract-text --help                                                                                                                                                                                                                                                        
 Usage: pdfly extract-text [OPTIONS] PDF                                        
                                                                                
 Extract text from a PDF file.                                                  
                                                                                
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf      FILE  [default: None] [required]                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the 10th page of `document.pdf` and extract the text inside of it, redirecting the output text into `page.txt`.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf

```
