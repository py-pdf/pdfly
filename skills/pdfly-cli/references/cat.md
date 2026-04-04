# Cat Command Reference

Extracts and concatenates pages from PDF files into a single PDF file. Can split or merge PDFs.

## Usage

```bash
pdfly cat FILENAME [FN_PGRGS...] -o OUTPUT [--verbose] [--password PASS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `FILENAME` | Input PDF file |
| `FN_PGRGS` | Filenames and/or page ranges |

A file not followed by a page range means **all pages** of that file.

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | **Required.** Output file path |
| `--verbose` | Show page ranges as they're read |
| `--password` | Password for encrypted PDFs |

## Page Range Syntax

Page ranges use Python slice notation. Remember: **page indices start with zero**.

| Expression | Meaning |
|------------|---------|
| `:` | All pages |
| `-1` | Last page |
| `22` | Page 23 (0-indexed) |
| `:3` | First 3 pages |
| `0:3` | Pages 0, 1, 2 |
| `5:` | From page 6 to end |
| `-2` | Second-to-last page |
| `-2:` | Last 2 pages |
| `-3:-1` | Third & second to last |

### Stride/Step

| Expression | Meaning |
|------------|---------|
| `::2` | Every other page (0, 2, 4...) |
| `1:10:2` | Pages 1, 3, 5, 7, 9 |
| `::-1` | All pages in reverse |

### Negative Indices with `--`

When using negative indices, use `--` to separate from command options:

```bash
pdfly cat input.pdf -- -1              # Last page only
pdfly cat input.pdf -- :-1            # All but last
```

## Examples

### Split a PDF - Extract pages 1-3

```bash
pdfly cat input.pdf 1:4 -o out.pdf
```

### Extract a single page (page 5, which is index 5)

```bash
pdfly cat input.pdf 5 -o out.pdf
```

### Concatenate two PDFs

```bash
pdfly cat input1.pdf input2.pdf -o out.pdf
```

### Complex merge

```bash
# All of head.pdf + pages 0-5 of content.pdf + last page of tail.pdf
pdfly cat head.pdf content.pdf :6 -1 tail.pdf -o output.pdf
```

### Verbose output

```bash
pdfly cat input.pdf 1:4 -o out.pdf --verbose
```

### Encrypted PDF

```bash
pdfly cat encrypted.pdf 1:5 -o out.pdf --password "userpass"
```

## Common Use Cases

| Task | Command |
|------|---------|
| Extract pages 1-3 | `pdfly cat in.pdf 1:4 -o out.pdf` |
| Remove page 2 | `pdfly cat in.pdf :2 3: -o out.pdf` |
| Reverse all pages | `pdfly cat in.pdf ::-1 -o out.pdf` |
| Every other page | `pdfly cat in.pdf ::2 -o out.pdf` |
| Last 5 pages | `pdfly cat in.pdf -5: -o out.pdf` |
