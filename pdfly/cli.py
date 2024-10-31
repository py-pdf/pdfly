"""
Define how the CLI should behave.

Subcommands are added here.
"""

from pathlib import Path
from typing import List

import typer
from typing_extensions import Annotated

import pdfly.cat
import pdfly.compress
import pdfly.extract_images
import pdfly.metadata
import pdfly.pagemeta
import pdfly.rm
import pdfly.up2
import pdfly.x2pdf


def version_callback(value: bool) -> None:
    import pypdf

    if value:
        typer.echo(f"pdfly {pdfly.__version__}")
        typer.echo(f"  using pypdf=={pypdf.__version__}")
        raise typer.Exit


entry_point = typer.Typer(
    add_completion=False,
    help=(
        "pdfly is a pure-python cli application for manipulating PDF files."
    ),
    rich_markup_mode="rich",  # Allows to pretty-print commands documentation
)


@entry_point.callback()  # type: ignore[misc]
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
) -> None:
    pass


@entry_point.command(name="extract-images", help=pdfly.extract_images.__doc__)  # type: ignore[misc]
def extract_images(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ]
) -> None:
    pdfly.extract_images.main(pdf)


@entry_point.command(name="2-up", help=pdfly.up2.__doc__)  # type: ignore[misc]
def up2(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    out: Path,
) -> None:
    pdfly.up2.main(pdf, out)


@entry_point.command(name="cat", help=pdfly.cat.__doc__)  # type: ignore[misc]
def cat(
    filename: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Path = typer.Option(..., "-o", "--output"),  # noqa
    fn_pgrgs: List[str] = typer.Argument(  # noqa
        ..., help="filenames and/or page ranges"
    ),
    verbose: bool = typer.Option(
        False, help="show page ranges as they are being read"
    ),
) -> None:
    pdfly.cat.main(filename, fn_pgrgs, output, verbose)


@entry_point.command(name="rm", help=pdfly.rm.__doc__)
def rm(
    filename: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Path = typer.Option(..., "-o", "--output"),  # noqa
    fn_pgrgs: List[str] = typer.Argument(  # noqa
        ..., help="filenames and/or page ranges"
    ),
    verbose: bool = typer.Option(
        False, help="show page ranges as they are being read"
    ),
) -> None:
    pdfly.rm.main(filename, fn_pgrgs, output, verbose)


@entry_point.command(name="meta", help=pdfly.metadata.__doc__)  # type: ignore[misc]
def metadata(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: pdfly.metadata.OutputOptions = typer.Option(  # noqa
        pdfly.metadata.OutputOptions.text.value,
        "--output",
        "-o",
        help="output format",
        show_default=True,
    ),
) -> None:
    pdfly.metadata.main(pdf, output)


@entry_point.command(name="pagemeta", help=pdfly.pagemeta.__doc__)  # type: ignore[misc]
def pagemeta(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    page_index: int,
    output: pdfly.metadata.OutputOptions = typer.Option(  # noqa
        pdfly.metadata.OutputOptions.text.value,
        "--output",
        "-o",
        help="output format",
        show_default=True,
    ),
) -> None:
    pdfly.pagemeta.main(
        pdf,
        page_index,
        output,
    )


@entry_point.command(name="extract-text")  # type: ignore[misc]
def extract_text(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ]
) -> None:
    """Extract text from a PDF file."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    for page in reader.pages:
        print(page.extract_text())


@entry_point.command(name="compress", help=pdfly.compress.__doc__)  # type: ignore[misc]
def compress(
    pdf: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Annotated[
        Path,
        typer.Argument(
            exists=False,
            writable=True,
        ),
    ],
) -> None:
    pdfly.compress.main(pdf, output)

@entry_point.command(name="x2pdf", help=pdfly.x2pdf.__doc__)
def x2pdf(
    x: List[Path],
    output: Annotated[
        Path,
        typer.Option(
            "-o",
            "--output",
            exists=False,
            writable=True,
        ),
    ],
    format: str = typer.Option(
        None,
        "--format",
        help="Optional page format for output PDF: Letter, A4-portrait, A4-landscape, or custom dimensions (e.g., 210x297). If omitted, no format is enforced."
    ),
) -> int:
    return pdfly.x2pdf.main(x, output, format)