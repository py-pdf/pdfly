# 2-up

Create a booklet-style PDF from a single input.

## Usage

```
$ pdfly 2-up --help
 Usage: pdfly 2-up [OPTIONS] PDF OUT

 Create a booklet-style PDF from a single input.

 Pairs of two pages will be put on one page (left and right)

 usage: python 2-up.py input_file output_file

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf      FILE  [default: None] [required]                               │
│ *    out      PATH  [default: None] [required]                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --password        TEXT  Document's user or owner password. [default: None]  │
│ --help                   Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

Convert `document.pdf` into a booklet and write the output in `booklet.pdf`.
```
pdfly 2-up document.pdf booklet.pdf

```

Convert a password-protected `document.pdf` into a booklet.
```
pdfly 2-up --password=SECRET document.pdf booklet.pdf

```