# extract-images

Extract text from a PDF file.
## Usage

```
$ pdfly extract-images --help
 Usage: pdfly extract-images [OPTIONS] PDF

 Extract images from PDF without resampling or altering.

 Adapted from work by Sylvain Pelissier
 http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python

┌─ Arguments ───────────────────────────────────────────────────────────────────────────────────────┐
│ *    pdf      FILE  [required]                                                                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─ Options ─────────────────────────────────────────────────────────────────────────────────────────┐
│ --output-dir  -o      DIRECTORY  Output directory. Defaults to the input's directory.             │
│ --help                           Show this message and exit.                                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘

  ```

## Examples

Extract the first page of `document.pdf` and extract the images present in it.

```
pdfly cat document.pdf 0 -o page.pdf

pdfly extract-images page.pdf
 Extracted 1 images:
 - 0-Image0.png

```

Extract the images of `document.pdf` in its directory's parent directory.

```
pdfly extract-images document.pdf -o ..
 Extracted 1 images:
 - <parent_directory>/0-Image0.png
 Stored in <parent_directory>

```
