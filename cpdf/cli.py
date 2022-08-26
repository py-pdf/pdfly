from pathlib import Path
from typing import List

import typer

import cpdf.cat
import cpdf.compress
import cpdf.extract_images
import cpdf.metadata
import cpdf.up2
import cpdf.offset_updater


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"cpdf {cpdf.__version__}")
        raise typer.Exit()


entry_point = typer.Typer(
    add_completion=False,
    help=("cpdf is a pure-python cli application for manipulating PDF files."),
)


@entry_point.callback()  # type: ignore[misc]
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),  # noqa
) -> None:
    pass


@entry_point.command(name="extract-images")  # type: ignore[misc]
def extract_images(pdf: Path) -> None:
    cpdf.extract_images.main(pdf)


@entry_point.command(name="2-up")  # type: ignore[misc]
def up2(pdf: Path, out: Path) -> None:
    cpdf.up2.main(pdf, out)


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
    cpdf.cat.main(filename, fn_pgrgs, output, verbose)


@entry_point.command(name="meta")  # type: ignore[misc]
def metadata(
    pdf: Path,
    output: cpdf.metadata.OutputOptions = typer.Option(  # noqa
        cpdf.metadata.OutputOptions.text.value,
        "--output",
        "-o",
        help="output format",
        show_default=True,
    ),
) -> None:
    cpdf.metadata.main(pdf, output)


@entry_point.command(name="extract-text")  # type: ignore[misc]
def extract_text(pdf: Path):
    """Extract text from a PDF file."""
    from PyPDF2 import PdfReader

    reader = PdfReader(str(pdf))
    for page in reader.pages:
        print(page.extract_text())


@entry_point.command(name="compress")  # type: ignore[misc]
def compress(pdf: Path, output: Path):
    cpdf.compress.main(pdf, output)


@entry_point.command(name="offset-updater")  # type: ignore[misc]
def offset_updater(
    file_in: Path,
    file_out: Path,
    encoding: str = typer.Option(
        "UTF-8",
        help="Encoding used to read and write the files, e.g. ISO-8859-1.",
    ),  # noqa
    verbose: bool = typer.Option(False, help="Show progress while processing."),  # noqa
) -> None:
    cpdf.offset_updater.main(file_in, file_out, encoding, verbose)


up2.__doc__ = cpdf.up2.__doc__
extract_images.__doc__ = cpdf.extract_images.__doc__
cat.__doc__ = cpdf.cat.__doc__
metadata.__doc__ = cpdf.metadata.__doc__
compress.__doc__ = cpdf.compress.__doc__
offset_updater.__doc__ = cpdf.offset_updater.__doc__
