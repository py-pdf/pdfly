# Rotate Command Reference

Rotates specified pages by the specified amount (90, 180, or 270 degrees).

## Usage

```bash
pdfly rotate -o OUTPUT INPUT DEGREES [PAGE_RANGE]
```

**Important:** `-o/--output` is **required** and must come **before** positional arguments.

## Arguments

| Argument | Description |
|----------|-------------|
| `INPUT` | Input PDF file |
| `DEGREES` | Rotation amount (90, 180, 270) |
| `PAGE_RANGE` | Pages to rotate (default: all pages) |

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | **Required.** Output file path |
| `--help` | Show help |

## Examples

### Rotate all pages by 90 degrees

```bash
pdfly rotate -o output.pdf input.pdf 90
```

### Rotate first 3 pages by 90 degrees

```bash
pdfly rotate -o output.pdf input.pdf 90 :3
```

### Rotate last page by 90 degrees

```bash
pdfly rotate -o output.pdf input.pdf 90 -- -1
```

### Rotate pages 1-3 by 180 degrees

```bash
pdfly rotate -o output.pdf input.pdf 180 "1-3"
```

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

### Negative Indices with `--`

When using negative indices, use `--` to separate from command options:

```bash
pdfly rotate -o output.pdf input.pdf 90 -- -1    # Last page
pdfly rotate -o output.pdf input.pdf 90 -- -2     # Second-to-last
```

### Stride/Step

| Expression | Meaning |
|------------|---------|
| `::2` | Every other page (0, 2, 4...) |
| `1:10:2` | Pages 1, 3, 5, 7, 9 |
| `::-1` | All pages in reverse |
| `2::-1` | Pages 2, 1, 0 |
