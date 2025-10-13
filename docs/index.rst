Welcome to pdfly
================

.. image:: https://img.shields.io/pypi/v/pdfly.svg
   :target: https://pypi.org/pypi/pdfly#history
.. image:: https://img.shields.io/pypi/pyversions/pdfly.svg
   :target: https://pypi.org/project/pdfly/
.. image:: https://img.shields.io/badge/License-BSD%203%20Clause-blue.svg
   :target: https://opensource.org/license/bsd-3-clause
.. image:: https://app.readthedocs.org/projects/pdfly/badge/?version=latest
   :target: https://pdfly.readthedocs.io/en/latest/

.. image:: https://github.com/py-pdf/pdfly/workflows/CI/badge.svg
   :target: https://github.com/py-pdf/pdfly/actions?query=branch%3Amain
.. image:: https://img.shields.io/github/last-commit/py-pdf/pdfly
   :target: https://github.com/py-pdf/pdfly/commits/main/
.. image:: https://img.shields.io/github/issues-closed/py-pdf/pdfly
   :target: https://github.com/py-pdf/pdfly/issues
.. image:: https://img.shields.io/github/issues-pr-closed/py-pdf/pdfly
   :target: https://github.com/py-pdf/pdfly/pulls

.. image:: https://img.shields.io/badge/linters-black,ruff,mypi-green.svg
   :target: https://github.com/py-pdf/pdfly/actions
.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat
   :target: https://makeapullrequest.com
.. image:: https://img.shields.io/badge/first--timers--only-friendly-blue.svg
   :target: https://www.firsttimersonly.com/

pdfly (say: PDF-li) is a pure-python cli application for manipulating PDF files.

.. image:: ./pdfly-logo.png
   :scale: 25%

Installation
------------

.. code-block::

    pip install -U pdfly

As ``pdfly`` is an application, you might want to install it with `pipx <https://pypi.org/project/pipx/>`__ or `uv tool <https://docs.astral.sh/uv/concepts/tools/>`__.

Usage
-----

.. code-block::

    $ pdfly --help

    Usage: pdfly [OPTIONS] COMMAND [ARGS]...

    pdfly is a pure-python cli application for manipulating PDF files.

    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --version                                                                                                                │
    │ --help             Show this message and exit.                                                                           │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ 2-up                      Create a booklet-style PDF from a single input.                                                │
    │ booklet                   Reorder and two-up PDF pages for booklet printing.                                             │
    │ cat                       Concatenate pages from PDF files into a single PDF file.                                       │
    │ check-sign                Verifies the signature of a signed PDF.                                                        │
    │ compress                  Compress a PDF.                                                                                │
    │ extract-annotated-pages   Extract only the annotated pages from a PDF.                                                   │
    │ extract-images            Extract images from PDF without resampling or altering.                                        │
    │ extract-text              Extract text from a PDF file.                                                                  │
    │ meta                      Show metadata of a PDF file                                                                    │
    │ pagemeta                  Give details about a single page.                                                              │
    │ rm                        Remove pages from PDF files.                                                                   │
    │ rotate                    Rotate specified pages by the specified amount                                                 │
    │ sign                      Creates a signed PDF from an existing PDF file.                                                │
    │ uncompress                Module for uncompressing PDF content streams.                                                  │
    │ update-offsets            Updates offsets and lengths in a simple PDF file.                                              │
    │ x2pdf                     Convert one or more files to PDF. Each file is a page.                                         │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

You can see the help of every subcommand by typing ``--help``:

.. code-block::

    $ pdfly 2-up --help

    Usage: pdfly 2-up [OPTIONS] PDF OUT

    Create a booklet-style PDF from a single input.
    Pairs of two pages will be put on one page (left and right)

    usage: python 2-up.py input_file output_file

    ╭─ Arguments ──────────────────────────────────────────────────────────────────────────╮
    │ *    pdf      PATH  [default: None] [required]                                       │
    │ *    out      PATH  [default: None] [required]                                       │
    ╰──────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────╯

.. toctree::
   :caption: User Guide
   :maxdepth: 1

   user/installation
   user/subcommand-2-up
   user/subcommand-booklet
   user/subcommand-cat
   user/subcommand-check-sign
   user/subcommand-compress
   user/subcommand-extract-annotated-pages
   user/subcommand-extract-images
   user/subcommand-extract-text
   user/subcommand-meta
   user/subcommand-pagemeta
   user/subcommand-rm
   user/subcommand-rotate
   user/subcommand-sign
   user/subcommand-uncompress
   user/subcommand-update-offsets
   user/subcommand-x2pdf

.. toctree::
   :caption: Developer Guide
   :maxdepth: 1

   dev/intro
   dev/testing

.. toctree::
   :caption: About pdfly
   :maxdepth: 1

   meta/CHANGELOG
   meta/CONTRIBUTORS
   meta/project-governance

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
