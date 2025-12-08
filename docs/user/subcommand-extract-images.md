# extract-images

Extract images from a PDF file. Supports selecting a range.
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
│ --from INTEGER   Inclusive starting image index (0-based).                   │
│ --end INTEGER    Inclusive ending image index (0-based).                     │
│ --help           Show this message and exit.                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Extract the first page of `document.pdf` and extract the images present in it.

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-images page.pdf
 Extracted 1 images:
 - 0009-Im0.png

Extract only specific images (by global index across the file):

```
pdfly extract-images document.pdf --from 0 --end 0   # only the first image
pdfly extract-images document.pdf --from 2            # from index 2 to the last
pdfly extract-images document.pdf --end 5             # from start to index 5
```

```
