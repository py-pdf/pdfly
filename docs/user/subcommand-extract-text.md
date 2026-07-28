# extract-text

Extract text from PDF files, optionally restricted to specific pages.

## Usage

```
$ pdfly extract-text --help
 Usage: pdfly extract-text [OPTIONS] FILENAME [FN_PGRGS]...

 Extract text from PDF files, optionally restricted to specific pages.

 Multiple files may be given, each optionally followed by a page range
 that applies to the file named immediately before it. A file not
 followed by a page range means all the pages of that file. Text is
 printed in the order the files and page ranges are given.

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

 Examples
    pdfly extract-text report.pdf
        Print the text of every page of report.pdf.

    pdfly extract-text report.pdf :5
        Print the text of the first five pages of report.pdf.

    pdfly extract-text intro.pdf :3 body.pdf -- -1
        Print the text of the first three pages of intro.pdf, followed
        by the text of the last page of body.pdf.

    pdfly extract-text report.pdf --output extracted.txt
        Write the extracted text to extracted.txt instead of stdout.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    filename      FILE         [default: None] [required]                   │
│      fn_pgrgs      FN_PGRGS...  filenames and/or page ranges [default: None] │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output    -o      PATH  Write text to a file instead of stdout.            │
│                           [default: None]                                   │
│ --password          TEXT  Document's user or owner password.                │
│                           [default: None]                                   │
│ --help                    Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

### Extract the text of an entire document

If you give `extract-text` just a filename and no page range, it treats
that as "all pages" — the same as an explicit `:` range — and prints the
text of every page, in order, to stdout.

```
pdfly extract-text document.pdf
```

### Extract the text of a single page

Page ranges use zero-based indices, so the 10th page of a document is
index `9`, not `10`. You can pull a single page out into its own file
first with `cat` and then run `extract-text` on that:

```
pdfly cat document.pdf 9 -o page.pdf

pdfly extract-text page.pdf
```

But since `extract-text` accepts a page range directly, you don't need
the intermediate file at all — just give the filename followed by the
page index:

```
pdfly extract-text document.pdf 9
```

Both commands produce identical output; the second is just shorter.

### Extract text from a range of pages

Page ranges follow Python slice syntax. `:5` means "everything before
index 5", i.e. the first five pages (indices 0-4):

```
pdfly extract-text report.pdf :5
```

Other useful ranges: `5:` (from the sixth page to the end), `2:8`
(pages 3 through 8), `::2` (every other page), and `::-1` (all pages,
reversed). See the full slice-syntax table in the `--help` output above.

### Extract a page counted from the end

Negative indices count backward from the last page (`-1` is the last
page, `-2` is the second-to-last, and so on). Because a leading `-`
would otherwise be parsed as a command-line option, you must insert a
bare `--` immediately before any negative range to tell pdfly "the rest
of these are positional arguments, not options":

```
pdfly extract-text report.pdf -- -1
```

This prints just the text of the last page of `report.pdf`.

### Extract text across multiple files

You can pass several files in one command, each optionally followed by
its own page range. A file with no range after it means "all of that
file's pages." Ranges apply only to the file named immediately before
them, and output is printed in the order you list things:

```
pdfly extract-text intro.pdf :3 body.pdf -- -1
```

This prints the first three pages of `intro.pdf` (indices 0-2),
followed by the last page of `body.pdf`. Note that only one `--` is
needed even though it applies to the last range in the list — see the
next section for why it has to go there.

### Write extracted text to a file

By default, text is printed to stdout. Use `--output`/`-o` to write it
to a file instead:

```
pdfly extract-text report.pdf --output extracted.txt
```

### Decrypt a password-protected document

If the PDF is encrypted, supply its user or owner password with
`--password`. pdfly decrypts the file in memory before extracting text
— it doesn't modify the original file:

```
pdfly extract-text --password=SECRET document.pdf
```

## Important: ordering `--password`/`--output` with negative page ranges

The `--` marker doesn't just apply to the one negative number next to
it — once pdfly's argument parser sees `--`, it treats **everything
after it** as positional arguments (filenames and page ranges), not as
options. That means `--password` and `--output` must appear **before**
the `--`, and the `-- <negative range>` portion should be the last
thing on the command line.

**Correct** — options come first, `-- -1` comes last:

```
pdfly extract-text --password=SECRET --output extracted.txt document.pdf -- -1
```

**Incorrect** — putting `--output` after the `--` means it gets
swallowed up as a positional argument (a bogus "filename") instead of
being parsed as an option, and the command will fail or behave
unexpectedly:

```
pdfly extract-text document.pdf -- -1 --output extracted.txt
```

The same rule applies any time you combine `--password`/`--output` with
a file that ends in a negative page range — always finish the command
with the `--`-prefixed negative range, and put every option ahead of it.