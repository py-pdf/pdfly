# uncompress

Module for uncompressing PDF content streams.
## Usage

```
$ pdfly ucompress --help
 Module for uncompressing PDF content streams.

 ╭─ Arguments ───────────────────────────────────────────╮
 │ *    pdf         FILE  [default: None] [required]     │
 │ *    output      PATH  [default: None] [required]     │
 ╰───────────────────────────────────────────────────────╯
 ╭─ Options ─────────────────────────────────────────────╮
 │ --help          Show this message and exit.           │
 ╰───────────────────────────────────────────────────────╯
```

## Examples

Uncompress `document_compressed.pdf` and output `document.pdf`.

```
pdfly uncompress document_compressed.pdf document.pdf
```