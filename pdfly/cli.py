from pathlib import Path
from typing import List

import typer

import pdfly.cat
import pdfly.compress
import pdfly.extract_images
import pdfly.metadata
import pdfly.up2


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pdfly {pdfly.__version__}")
        raise typer.Exit()


entry_point = typer.Typer(
    add_completion=False,
    help=("pdfly is a pure-python cli application for manipulating PDF files."),
)


@entry_point.callback()  # type: ignore[misc]
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),  # noqa
) -> None:
    pass


@entry_point.command(name="extract-images")  # type: ignore[misc]
def extract_images(pdf: Path) -> None:
    pdfly.extract_images.main(pdf)


@entry_point.command(name="2-up")  # type: ignore[misc]
def up2(pdf: Path, out: Path) -> None:
    pdfly.up2.main(pdf, out)


@entry_point.command(name="cat")  # type: ignore[misc]
def cat(
    filename: Path,
    output: Path = typer.Option(..., "-o", "--output"),  # noqa
    fn_pgrgs: List[str] = typer.Argument(  # noqa
        ..., help="filenames and/or page ranges"
    ),
    verbose: bool = typer.Option(  # noqa
        False, help="show page ranges as they are being read"
    ),
) -> None:
    pdfly.cat.main(filename, fn_pgrgs, output, verbose)


@entry_point.command(name="meta")  # type: ignore[misc]
def metadata(
    pdf: Path,
    output: pdfly.metadata.OutputOptions = typer.Option(  # noqa
        pdfly.metadata.OutputOptions.text.value,
        "--output",
        "-o",
        help="output format",
        show_default=True,
    ),
) -> None:
    pdfly.metadata.main(pdf, output)


@entry_point.command(name="extract-text")  # type: ignore[misc]
def extract_text(pdf: Path):
    """Extract text from a PDF file."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    for page in reader.pages:
        print(page.extract_text())


@entry_point.command(name="compress")  # type: ignore[misc]
def compress(pdf: Path, output: Path):
    pdfly.compress.main(pdf, output)


up2.__doc__ = pdfly.up2.__doc__
extract_images.__doc__ = pdfly.extract_images.__doc__
cat.__doc__ = pdfly.cat.__doc__
metadata.__doc__ = pdfly.metadata.__doc__
compress.__doc__ = pdfly.compress.__doc__
