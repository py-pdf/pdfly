# compress

Compress a PDF using lossless FlateDecode compression.

**Note:** If compression would result in a larger file, the original file is kept unchanged to avoid file size increase.

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
```
## Examples

Compress the file `document.pdf` and output `document_compressed.pdf`

```
pdfly compress document.pdf document_compressed.pdf
```

Example output when compression succeeds:
```
Original Size  : 1,996,123
Final Size     : 1,234,567 (Compressed (61.8% of original))
```

Example output when compression would increase file size:
```
Original Size  : 887
Final Size     : 887 (No compression applied (would increase size))
```
