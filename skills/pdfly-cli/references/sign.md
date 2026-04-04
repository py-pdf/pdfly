# PDF Signing Reference

## Sign Command

Creates a digitally-signed PDF from an existing PDF file and a PKCS12 certificate.

### Usage

```bash
pdfly sign FILENAME --p12 CERT.p12 [-o OUT.pdf] [-i] [-p PASSWORD]
```

### Options

| Option | Description |
|--------|-------------|
| `--p12` | **Required.** PKCS12 certificate container (.p12 or .pfx) |
| `-o, --output` | Output file path |
| `-i, --in-place` | Modify input file directly |
| `-p, --p12-password` | Password to decrypt PKCS12 file |

### Examples

```bash
# Sign with PKCS12 certificate
pdfly sign input.pdf --p12 certs.p12 -o signed.pdf

# In-place signing (modifies original)
pdfly sign input.pdf --p12 certs.p12 --in-place

# With password
pdfly sign input.pdf --p12 certs.p12 -o signed.pdf -p "password"
```

---

## Check Signature Command

Verifies the digital signature of a signed PDF.

### Usage

```bash
pdfly check-sign FILENAME --pem CERT.pem [--verbose]
```

### Options

| Option | Description |
|--------|-------------|
| `--pem` | **Required.** PEM certificate file |
| `--verbose` | Show detailed verification info |

### Examples

```bash
# Basic verification
pdfly check-sign signed.pdf --pem certificate.pem

# With detailed output
pdfly check-sign signed.pdf --pem certificate.pem --verbose
```

---

## Complete Signing Workflow

1. **Create/Obtain a PKCS12 certificate** (`.p12` or `.pfx`)
   ```bash
   # Or convert from other formats using OpenSSL
   openssl pkcs12 -export -in cert.pem -inkey key.pem -out cert.p12
   ```

2. **Sign the PDF**:
   ```bash
   pdfly sign unsigned.pdf --p12 signing-certificate.p12 -o signed.pdf -p "your-password"
   ```

3. **Verify the signature**:
   ```bash
   pdfly check-sign signed.pdf --pem signing-certificate.pem
   ```

---

## Certificate Formats

| Format | Extension | Used With |
|--------|-----------|-----------|
| PKCS12 | `.p12`, `.pfx` | `sign --p12` |
| PEM | `.pem`, `.crt` | `check-sign --pem` |

Convert between formats:
```bash
# PKCS12 to PEM (for verification)
openssl pkcs12 -in cert.p12 -out cert.pem -nodes

# PEM to PKCS12 (for signing)
openssl pkcs12 -export -in cert.pem -inkey key.pem -out cert.p12
```
