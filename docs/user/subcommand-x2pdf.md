# x2pdf

Convert a file to PDF.

Currently supported for "x":

* PNG
* JPG


## Usage

```
$ pdfly x2pdf --help

 Usage: pdfly x2pdf [OPTIONS] X...

 Convert one or more files to PDF. Each file is a page.

╭─ Arguments ─────────────────────────────────────────────────────────────────╮
│ *    x      X...  [default: None] [required]                                │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────╮
│ *  --output  -o      PATH  [default: None] [required]                       │
│    --help                  Show this message and exit.                      │
╰─────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Single file

```
$ pdfly x2pdf image.jpg -o out.pdf
$ ls -lh
-rw-rw-r-- 1 user user 47K Sep 17 21:49 image.jpg
-rw-rw-r-- 1 user user 49K Sep 17 22:48 out.pdf
```

### Multiple files manually

```
$ pdfly x2pdf image1.jpg image2.jpg -o out.pdf
$ ls -lh
-rw-rw-r-- 1 user user 47K Sep 17 21:49 image1.jpg
-rw-rw-r-- 1 user user 15K Sep 17 21:49 image2.jpg
-rw-rw-r-- 1 user user 64K Sep 17 22:48 out.pdf
```

### Multiple files via *

```
$ pdfly x2pdf *.jpg -o out.pdf
$ ls -lh
-rw-rw-r-- 1 user user 47K Sep 17 21:49 image1.jpg
-rw-rw-r-- 1 user user 15K Sep 17 21:49 image2.jpg
-rw-rw-r-- 1 user user 64K Sep 17 22:48 out.pdf
```
