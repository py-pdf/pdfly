# extract-images

Extract images from a PDF file.
## Usage

```
$ pdfly extract-images --help
 Usage: pdfly extract-images [OPTIONS] PDF

 Extract images from PDF without resampling or altering.

 Adapted from work by Sylvain Pelissier
 http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-res
 ampling-in-python

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf      FILE  [default: None] [required]                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --password        TEXT  Document's user or owner password. [default: None]  │
│ --help                   Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the tenth page of `document.pdf` and extract the images present in it.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-images page.pdf
 Extracted 1 images:
 - 0000-Im0.png

```

Extract images from a password-protected document:

```
pdfly extract-images --password=SECRET document.pdf
```