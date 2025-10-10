"""Give details about a single page."""

from pathlib import Path

from pydantic import BaseModel
from pypdf import PdfReader
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from ._utils import OutputOptions

KNOWN_PAGE_FORMATS = {
    (841.89, 1190.55): "A3",
    (595.28, 841.89): "A4",
    (420.94, 595.28): "A5",
    (612, 792): "Letter",
    (612, 1008): "Legal",
}


class PageMeta(BaseModel):
    mediabox: tuple[float, float, float, float]
    cropbox: tuple[float, float, float, float]
    artbox: tuple[float, float, float, float]
    bleedbox: tuple[float, float, float, float]
    annotations: int
    rotation: int


def main(pdf: Path, page_index: int, output: OutputOptions) -> None:
    reader = PdfReader(pdf)
    page = reader.pages[page_index]
    meta = PageMeta(
        mediabox=page.mediabox,
        cropbox=page.cropbox,
        artbox=page.artbox,
        bleedbox=page.bleedbox,
        annotations=len(page.annotations) if page.annotations else 0,
        rotation=page.rotation,
    )

    if output == OutputOptions.json:
        print(meta.json())
    else:
        console = Console()
        table = Table(title=f"{pdf}, page index {page_index}")
        table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        table.add_column("Value", style="white")

        def add_box_attr(
            name: str, box: tuple[float, float, float, float]
        ) -> None:
            width = box[2] - box[0]
            height = box[3] - box[1]
            known_format = KNOWN_PAGE_FORMATS.get((width, height))
            extra = f" ({known_format})" if known_format else ""
            table.add_row(
                name,
                f"({box[0]:.2f}, {box[1]:.2f}, {box[2]:.2f}, {box[3]:.2f}):"
                f" {width=:.2f} x {height=:.2f}{extra}",
            )

        add_box_attr("mediabox", meta.mediabox)
        add_box_attr("cropbox", meta.cropbox)
        add_box_attr("artbox", meta.artbox)
        add_box_attr("bleedbox", meta.bleedbox)

        if meta.annotations:
            table.add_row("annotations", str(meta.annotations))
        if meta.rotation:
            table.add_row("rotation", str(meta.rotation))

        console.print(table)

        if page.annotations:
            console.print(Markdown("**All annotations:**"))
            for i, annot in enumerate(page.annotations, start=1):
                obj = annot.get_object()
                console.print(f"{i}. {obj['/Subtype']} at {obj['/Rect']}")
