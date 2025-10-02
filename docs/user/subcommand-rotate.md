# rotate

## Usage

```
pdfly rotate --help

 Usage: pdfly rotate [OPTIONS] FILENAME DEGREES [PGRGS]

 Rotate specified pages by the specified amount

 Example:
     pdfly rotate --output output.pdf input.pdf 90
         Rotate all pages by 90 degrees (clockwise)

     pdfly rotate --output output.pdf input.pdf 90 :3
         Rotate first three pages by 90 degrees (clockwise)

     pdfly rotate --output output.pdf input.pdf 90 -- -1
         Rotate last page by 90 degrees (clockwise)

 A file not followed by a page range (PGRGS) means all the pages of the file.

 PAGE RANGES are like Python slices.

         Remember, page indices start with zero.

         When using page ranges that start with a negative value a
         two-hyphen symbol -- must be used to separate them from
         the command line options.

         Page range expression examples:

             :     all pages.                   -1    last page.
             22    just the 23rd page.          :-1   all but the last page.
             0:3   the first three pages.       -2    second-to-last page.
             :3    the first three pages.       -2:   last two pages.
             5:    from the sixth page onward.  -3:-1 third & second to last.

         The third, "stride" or "step" number is also recognized.

             ::2       0 2 4 ... to the end.    3:0:-1    3 2 1 but not 0.
             1:10:2    1 3 5 7 9                2::-1     2 1 0.
             ::-1      all pages in reverse order.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    filename      FILE     [required]                                                                                                                                                     │
│ *    degrees       INTEGER  degrees to rotate [required]                                                                                                                                   │
│      pgrgs         [PGRGS]  page range [default: :]                                                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --output  -o      PATH  [required]                                                                                                                                                      │
│    --help                  Show this message and exit.                                                                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Rotate all pages by 90 degrees (clockwise)

Rotate all pages from `input.pdf` by 90 degrees (clockwise) and write the resulting pdf to `output.pdf`.

```
pdfly rotate --output output.pdf input.pdf 90
```

### Rotate first three pages by 90 degrees (clockwise)

Rotate first three pages from `input.pdf` by 90 degrees (clockwise) and write the resulting pdf to `output.pdf`.

```
pdfly rotate --output output.pdf input.pdf 90 :3
```

### Rotate last page by 90 degrees (clockwise)

Rotate last page from `input.pdf` by 90 degrees (clockwise) and write the resulting pdf to `output.pdf`.

```
pdfly rotate --output output.pdf input.pdf 90 -- -1
```
