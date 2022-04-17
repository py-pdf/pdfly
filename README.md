[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/cpdf.svg)](https://pypi.org/project/cpdf/)
[![GitHub last commit](https://img.shields.io/github/last-commit/py-pdf/cpdf)](https://github.com/py-pdf/cpdf)
[![Python Support](https://img.shields.io/pypi/pyversions/cpdf.svg)](https://pypi.org/project/cpdf/)

# cpdf

cpdf is a pure-python cli application for manipulating PDF files.

## Installation

```bash
pip install -U cpdf
```

As `cpdf` is an application, you might want to install it with [`pipx`](https://pypi.org/project/pipx/).

## Usage

```console
$ cpdf --help
Usage: cpdf [OPTIONS] COMMAND [ARGS]...

  cpdf is a pure-python cli application for manipulating PDF files.

Options:
  --version
  --help     Show this message and exit.

Commands:
  2-up            Create a booklet-style PDF from a single input.
  cat             Concatenate pages from PDF files into a single PDF file.
  extract-images  Extract images from PDF without resampling or altering.
```

You can see the help of every subcommand by typing:

```console
$ cpdf 2-up --help
Usage: cpdf 2-up [OPTIONS] PDF OUT

  Create a booklet-style PDF from a single input.

  Pairs of two pages will be put on one page (left and right)

  usage: python 2-up.py input_file output_file

Arguments:
  PDF  [required]
  OUT  [required]

Options:
  --help  Show this message and exit.
```
