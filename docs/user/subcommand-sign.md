# sign

Creates a digitally-signed PDF from an existing PDF file and a given certificate.

## Usage

```
$ pdfly sign --help
 Usage: pdfly sign [OPTIONS] {filename}

 Creates a signed PDF from an existing PDF file.

 Examples
 pdfly sign input.pdf --p12 certs.p12 -o signed.pdf

     Signs the input.pdf with a PKCS12 certificate archive. Writes the
 resulting signed pdf into signed.pdf.

 pdfly sign document.pdf --p12 certs.p12 --in-place

     Signs the document.pdf with a PKCS12 certificate archive. Modifies the
 input file in-place.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    filename      <file>  [required]                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --p12                   <file>  PKCS12 certificate container [required]   │
│    --output        -o      <path>                                            │
│    --in-place      -i      <bool>                                            │
│    --p12-password  -p      <str>   The password to use to decrypt the PKCS12 │
│                                    file.                                     │
│    --help                  <bool>  Show this message and exit.               │
╰──────────────────────────────────────────────────────────────────────────────╯
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
