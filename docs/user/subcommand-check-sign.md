# check-sign

## Usage

```
 Usage: pdfly check-sign [OPTIONS] FILENAME

 Verifies the signature of a signed PDF.

 Examples
 pdfly verify input.pdf --pem certs.pem

     Verifies the input.pdf with a PEM certificate bundle.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    filename      FILE  [required]                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --pem                        FILE  PEM certificate file [required]                                                            │
│    --verbose    --no-verbose          Show signature verification details. [default: no-verbose]                                 │
│    --help                             Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Verify PDF signature against a PEM certificate

Verifies the input.pdf with a PEM certificate bundle.

```
pdfly verify input.pdf --pem certs.pem
```
