[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/pdfly.svg)](https://pypi.org/project/pdfly/)
[![GitHub last commit](https://img.shields.io/github/last-commit/py-pdf/pdfly)](https://github.com/py-pdf/pdfly)
[![Python Support](https://img.shields.io/pypi/pyversions/pdfly.svg)](https://pypi.org/project/pdfly/)

# pdfly

pdfly (say: PDF-li) is a pure-python cli application for manipulating PDF files.

## Installation

```bash
pip install -U pdfly
```

As `pdfly` is an application, you might want to install it with [`pipx`](https://pypi.org/project/pipx/).

## Usage

```console
$ pdfly --help

 Usage: pdfly [OPTIONS] COMMAND [ARGS]...

 pdfly is a pure-python cli application for manipulating PDF files.

╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --version                                                                   │
│ --help             Show this message and exit.                              │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────╮
│ 2-up             Create a booklet-style PDF from a single input.            │
│ cat              Concatenate pages from PDF files into a single PDF file.   │
│ compress         Compress a PDF.                                            │
│ extract-images   Extract images from PDF without resampling or altering.    │
│ extract-text     Extract text from a PDF file.                              │
│ meta             Show metadata of a PDF file                                │
│ pagemeta         Give details about a single page.                          │
╰─────────────────────────────────────────────────────────────────────────────╯
```

You can see the help of every subcommand by typing:

```console
$ pdfly 2-up --help

 Usage: pdfly 2-up [OPTIONS] PDF OUT

 Create a booklet-style PDF from a single input.
 Pairs of two pages will be put on one page (left and right)
 usage: python 2-up.py input_file output_file

╭─ Arguments ─────────────────────────────────────────────────────────────────╮
│ *    pdf      PATH  [default: None] [required]                              │
│ *    out      PATH  [default: None] [required]                              │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                 │
╰─────────────────────────────────────────────────────────────────────────────╯
```
