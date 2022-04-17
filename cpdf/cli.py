from pathlib import Path
from typing import List

import typer
from PyPDF2.pagerange import PAGE_RANGE_HELP

import cpdf.cat
import cpdf.image_extractor
import cpdf.up2


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
    version: bool = typer.Option(None, "--version", callback=version_callback),
) -> None:
    pass


@entry_point.command(name="extract-images")  # type: ignore[misc]
def extract_images(pdf: Path) -> None:
    cpdf.image_extractor.main(pdf)


@entry_point.command(name="2-up")  # type: ignore[misc]
def up2(pdf: Path, out: Path) -> None:
    cpdf.up2.main(pdf, out)


@entry_point.command(name="cat")  # type: ignore[misc]
def cat(
    filename: Path,
    output: Path = typer.Option(..., "-o", "--output"),
    fn_pgrgs: List[str] = typer.Argument(..., help="filenames and/or page ranges"),
    verbose: bool = typer.Option(False, help="show page ranges as they are being read"),
) -> None:
    cpdf.cat.main(filename, fn_pgrgs, output, verbose)


cat.__doc__ = cpdf.cat.__doc__.format(page_range_help=PAGE_RANGE_HELP)
