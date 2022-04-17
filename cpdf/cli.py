from pathlib import Path
from typing import List

import typer

import cpdf.cat
import cpdf.extract_images
import cpdf.metadata
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
        ...,
        "--output",
        "-o",
        help="output format",
        show_default=True,
    ),
) -> None:
    cpdf.metadata.main(pdf, output)


up2.__doc__ = cpdf.up2.__doc__
extract_images.__doc__ = cpdf.extract_images.__doc__
cat.__doc__ = cpdf.cat.__doc__
metadata.__doc__ = cpdf.metadata.__doc__
