# decrypt

Remove password protection from an encrypted PDF file.

The decrypted PDF is written to `OUTPUT_FILE`. If `OUTPUT_FILE` is omitted,
the PDF is written to standard output, so the command can be used in pipes.

## Usage

```
$ pdfly decrypt --help

 Usage: pdfly decrypt [OPTIONS] [INPUT_FILE] [OUTPUT_FILE]

 Remove password protection from an encrypted PDF file.

 The decrypted PDF is written to OUTPUT_FILE. If OUTPUT_FILE is omitted,
 the PDF is written to standard output, so the command can be used in pipes.

 Examples
     pdfly decrypt encrypted.pdf decrypted.pdf

     pdfly decrypt --password secret encrypted.pdf > decrypted.pdf

     pdfly decrypt < encrypted.pdf > decrypted.pdf

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   input_file       <file>  Path to the encrypted PDF file, or '-' to read    │
│                            from STDIN.                                       │
│   output_file      <file>  Path where the decrypted PDF is written. If       │
│                            omitted, the PDF is written to standard output.   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --password  -p      <str>   The password required to decrypt the PDF.        │
│ --help              <bool>  Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

Decrypt the file `encrypted.pdf` using the password `secret`, writing the
result to `decrypted.pdf`:

```
pdfly decrypt --password secret encrypted.pdf decrypted.pdf
```

Write the decrypted PDF to standard output, e.g. to directly consume it in a
pipe:

```
pdfly decrypt --password secret encrypted.pdf | pdfly meta -
```

Without a password, an empty password is tried first. If that fails, the
command asks you to provide the password explicitly:

```
$ pdfly decrypt encrypted.pdf
Error: The PDF is encrypted. Please provide the password using --password.
```

Encrypted input can also be read from standard input:

```
pdfly decrypt -p secret < encrypted.pdf > decrypted.pdf
```
