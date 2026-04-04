# Page Range Syntax Reference

pdfly uses Python slice notation for page ranges. All page indices are **0-based** (first page is 0).

## Basic Syntax

| Expression | Meaning |
|------------|---------|
| `:` | All pages |
| `-1` | Last page |
| `22` | Page 23 (0-indexed) |
| `:3` | First 3 pages (0, 1, 2) |
| `0:3` | Pages 0, 1, 2 |
| `5:` | From page 6 to end |
| `-2` | Second-to-last page |
| `-2:` | Last 2 pages |
| `-3:-1` | Third & second to last |

## Stride/Step

The third part of Python slice syntax (step):

| Expression | Meaning |
|------------|---------|
| `::2` | Every other page (0, 2, 4...) |
| `1:10:2` | Pages 1, 3, 5, 7, 9 |
| `::-1` | All pages in reverse |
| `2::-1` | Pages 2, 1, 0 |
| `3:0:-1` | Pages 3, 2, 1 (not 0) |

## Negative Indices

Negative indices count from the end. When using negative values that look like options (e.g., `-1`), use `--` to separate from command options:

```bash
# Correct - last page
pdfly cat input.pdf -- -1 -o out.pdf

# Correct - all but last
pdfly cat input.pdf -- :-1 -o out.pdf
```

## Quick Reference Table

| Want | Use | Notes |
|------|-----|-------|
| All pages | `:` | Default if no range given |
| First N pages | `:N` | Pages 0 to N-1 |
| Last N pages | `-N:` | |
| Single page | `N` | 0-indexed |
| Pages M to N | `M:N` | Page M to N-1 |
| Every other | `::2` | Even pages |
| Odd pages | `1::2` | |
| Reverse | `::-1` | |
| Exclude page N | `:N N+1:` | Remove page N |

## Examples in Context

### cat command
```bash
pdfly cat in.pdf :10 -o out.pdf       # First 10 pages
pdfly cat in.pdf -3: -o out.pdf        # Last 3 pages
pdfly cat in.pdf ::2 -o out.pdf       # Even pages only
```

### rm command
```bash
pdfly rm in.pdf 5 -o out.pdf          # Remove page 6
pdfly rm in.pdf 2,4,6 -o out.pdf      # Remove pages 3, 5, 7
pdfly rm in.pdf 1:5 -o out.pdf        # Remove pages 2-5
```

### rotate command
```bash
pdfly rotate -o out.pdf in.pdf 90 :3     # Rotate first 3
pdfly rotate -o out.pdf in.pdf 90 5:     # Rotate from page 6
pdfly rotate -o out.pdf in.pdf 90 -- -1   # Rotate last page
```
