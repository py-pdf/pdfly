# cat

The cat command can split / extract pages from a PDF. It can also
join/merge/combine multiple PDF documents into a single one.


## Usage

```
pdfly cat --help

 Usage: pdfly cat [OPTIONS] FILENAME FN_PGRGS...

 Concatenate pages from PDF files into a single PDF file.
 Page ranges refer to the previously-named file. A file not followed by a page
 range means all the pages of the file.
 PAGE RANGES are like Python slices.
 Remember, page indices start with zero.
 When using page ranges that start with a negative value a
 two-hyphen symbol -- must be used to separate them from
 the command line options.
 Page range expression examples:

    :     all pages.
    -1    last page.
    22    just the  23rd page.
    :-1   all but the last page.
    0:3   the first   three pages.
    -2    second-to-last page.
    :3    the first      three pages.
    -2:   last two pages.
    5:    from the sixth page onward.
    -3:-1 third & second to last.

 The third, "stride" or "step" number is also recognized.

    ::2       0 2 4 ... to the end.
    3:0:-1    3 2 1 but not 0.
    1:10:2    1 3 5 7 9
    2::-1     2 1 0.
    ::-1      all  pages in reverse order.


 Examples
    pdfly cat -o output.pdf head.pdf -- content.pdf :6 7: tail.pdf -1
        Concatenate all of head.pdf, all but page seven of content.pdf,
        and the last page of tail.pdf, producing output.pdf.

    pdfly cat chapter*.pdf >book.pdf
        You can specify the output file by redirection.

    pdfly cat chapter?.pdf chapter10.pdf >book.pdf
        In case you don't want chapter 10 before chapter 2.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    filename      PATH         [default: None] [required]                   │
│ *    fn_pgrgs      FN_PGRGS...  filenames and/or page ranges [default: None] │
│                                 [required]                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --output   -o                  PATH  [default: None] [required]           │
│    --verbose      --no-verbose          show page ranges as they are being   │
│                                         read                                 │
│                                         [default: no-verbose]                │
│    --help                               Show this message and exit.          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Split a PDF

Get the second, third, and fourth page of a PDF:

```
pdfly cat input.pdf 1:4 -o out.pdf
```

### Extract a Page

Get the sixt page of a PDF:

```
pdfly cat input.pdf 5 -o out.pdf
```

Note that it is `5`, because the page indices always start at 0.

### Concatenate two PDFs

Just combine two PDF files so that the pages come right after each other:

```
pdfly cat input1.pdf input2.pdf -o out.pdf
```
