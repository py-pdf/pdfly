# meta

Compress a PDF.

## Usage

```
$ pdfly compress --help                                                                                                                                                                                                                                                        
 Usage: pdfly compress [OPTIONS] PDF OUTPUT                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                       
 Compress a PDF.

╭─ Arguments ───────────────────────────────────────────╮
│ *    pdf         FILE  [default: None] [required]     │
│ *    output      PATH  [default: None] [required]     │
╰───────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────╮
│ --help          Show this message and exit.           │
╰───────────────────────────────────────────────────────╯

## Examples

Compress the file `document.pdf` and output `document_compressed.pdf`

```
pdfly compress document.pdf document_compressed.pdf

```
