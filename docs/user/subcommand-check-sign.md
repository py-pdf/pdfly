# check-sign

Validate that a PDF document has a digital signature matching a given certificate.

## Usage

```
$ pdfly check-sign --help
 Usage: pdfly check-sign [OPTIONS] {filename}

 Verifies the signature of a signed PDF.

 Examples
 pdfly check-sign input.pdf --pem certs.pem

     Verifies the input.pdf with a PEM certificate bundle.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    filename      <file>  [required]                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --pem                        <file>  PEM certificate file [required]      │
│    --verbose    --no-verbose    <bool>  Show signature verification details. │
│                                         [default: no-verbose]                │
│    --help                       <bool>  Show this message and exit.          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Verify PDF signature against a PEM certificate

Verifies the input.pdf with a PEM certificate bundle.

```
pdfly check-sign input.pdf --pem certs.pem
```
