# meta

Get metadata of a PDF file.

## Usage

```
pdfly meta --help

 Usage: pdfly meta [OPTIONS] PDF

 Show metadata of a PDF file

╭─ Arguments ───────────────────────────────────────────────────────────────────╮
│ *    pdf      FILE  [default: None] [required]                                │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --output  -o      [json|text]  output format [default: text]                  │
│ --help                         Show this message and exit.                    │
╰───────────────────────────────────────────────────────────────────────────────╯
```

## Example

```
$pdfly meta Allianz-Versicherungsunterlagen.pdf

                              Operating System Data
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         Attribute ┃ Value                                                     ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│         File Name │ /home/user/Documents/Allianz-Versicherungsunterlagen.pdf  │
│  File Permissions │ -rw-rw-r--                                                │
│         File Size │ 874,781 bytes                                             │
│     Creation Time │ 2023-09-02 10:00:51                                       │
│ Modification Time │ 2023-09-02 10:00:42                                       │
│       Access Time │ 2023-09-09 11:57:41                                       │
└───────────────────┴───────────────────────────────────────────────────────────┘
                                    PDF Data
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          Attribute ┃ Value                                                    ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│              Title │                                                          │
│           Producer │ itext-paulo-155 (itextpdf.sf.net-lowagie.com)            │
│             Author │                                                          │
│              Pages │ 34                                                       │
│          Encrypted │ None                                                     │
│   PDF File Version │ %PDF-1.6                                                 │
│        Page Layout │                                                          │
│          Page Mode │                                                          │
│             PDF ID │ ID1=b"'\xc5\x92\xc3\x92\xe2\x80\x93--/\xef\xac\x824\xc3… │
│                    │ ID2=b'\xc3\x8b\xc3\xaa\xcb\x9b\r\xc3\xa2\r\xcb\x99T\xc3… │
│                    │ \xc3\x96\xc3\x9fY2'                                      │
│ Fonts (unembedded) │ /Helvetica                                               │
│   Fonts (embedded) │ /ASPNQQ+TT22D6t00, /CBKSHX+Helvetica-Bold,               │
│                    │ /CXQKAY+Helvetica, /GOCSXU+AllianzNeo-Bold,              │
│                    │ /LKNHUL+Arial-BoldMT, /LMNFKX+ArialMT, /MWUNIP+Symbol,   │
│                    │ /ODNMDG+TT5B6t00, /PESMKN+AllianzNeo-CondensedBold,      │
│                    │ /PHDALA+Helvetica-Oblique, /PJEFXS+AllianzNeo-Light,     │
│                    │ /SNDABN+Helvetica, /SNDABN+Helvetica-Bold,               │
│                    │ /SNDABN+Times-Roman, /TXDAYK+Helvetica,                  │
│                    │ /VORXLN+Helvetica-BoldOblique, /YTXZAH+Arial-ItalicMT    │
│        Attachments │ []                                                       │
│             Images │ 16 images (355,454 bytes)                                │
└────────────────────┴──────────────────────────────────────────────────────────┘
Use the 'pagemeta' subcommand to get details about a single page

```
