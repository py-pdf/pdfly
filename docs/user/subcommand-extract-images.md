# extract-images

Extract images from PDF without resampling or altering (see [issue #200](https://github.com/py-pdf/pdfly/issues/200))

## Usage

```
$ pdfly extract-images --help
 Usage: pdfly extract-images [OPTIONS] {pdf} [pgrgs]

 Extract images from PDF without resampling or altering.

 Adapted from work by Sylvain Pelissier
 http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-res
 ampling-in-python

 Example:
     pdfly extract-images input.pdf
         Extract the images from all pages

     pdfly extract-images input.pdf --output-dir images
         Extract the images into the images directory

     pdfly extract-images input.pdf 2
         Extract the images from the third page only

     pdfly extract-images input.pdf 0:3
         Extract the images from the first three pages

     pdfly extract-images input.pdf -- -1
         Extract the images from the last page

 PAGE RANGES are like Python slices: page indices start with zero.
 When using page ranges that start with a negative value, a two-hyphen
 symbol -- must be used to separate them from the command line options.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf        <file>  [required]                                           │
│      pgrgs      <str>   page range of the pages to extract images from       │
│                         [default: :]                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output-dir        <dir>   Directory where extracted images are written.    │
│ --help              <bool>  Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the first page of `document.pdf` and extract the images present in it.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf
 Extracted 1 images:
 - 0-Im0.png

```
