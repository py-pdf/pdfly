# sign

Creates a signed PDF from an existing PDF file.

## Usage

```
Usage: pdfly sign [OPTIONS] FILENAME

Creates a signed PDF.

Examples
pdfly sign input.pdf --p12 certs.p12 -o signed.pdf

    Signs the input.pdf with a PKCS12 certificate archive. Writes the resulting signed pdf into signed.pdf.

pdfly sign document.pdf --p12 certs.p12 --in-place

    Signs the document.pdf with a PKCS12 certificate archive. Modifies the input file in-place.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    filename      FILE  [required]                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --p12                   FILE  PKCS12 certificate container [required]                                                         │
│    --output        -o      PATH                                                                                                  │
│    --in-place      -i                                                                                                            │
│    --p12-password  -p      TEXT  The password to use to decrypt the PKCS12 file.                                                 │
│    --help                        Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Examples

### Sign a PDF with PKCS12

Signs the input.pdf with a PKCS12 certificate archive. Writes the resulting signed pdf into signed.pdf.

```
pdfly sign input.pdf --p12 certs.p12 -o signed.pdf
```

### Sign a PDF in-place

Signs the document.pdf with a PKCS12 certificate archive. Modifies the input file in-place.

```
pdfly sign document.pdf --p12 certs.p12 --in-place
```
