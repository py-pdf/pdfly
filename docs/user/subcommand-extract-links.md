# extract-links
Extract all links from a PDF document.

## Usage
```
$ pdfly extract-links --help

 Usage: pdfly extract-links [OPTIONS] {pdf}

 Extract all links from a PDF document.

╭─ Arguments ───────────────────────────────────────────────────╮
│ *    pdf      <file>  [required]                              │
╰───────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────╮
│ --format  -f      <json|text>  Output format [default: text]  │
│ --help            <bool>       Show this message and exit.    │
╰───────────────────────────────────────────────────────────────╯
```

## Examples
Extract all links from `doc.pdf` and pass them to `jq`:
```
pdfly extract-links doc.pdf --format json | jq -r .
```
