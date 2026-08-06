"""Extract all links from a PDF document."""

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel
from pypdf import PdfReader

if TYPE_CHECKING:
    from pypdf.generic import ArrayObject

from ._utils import OutputOptions


class UriLink(BaseModel):
    uri: str
    page: int
    rect: list[float]


def main(pdf: Path, output_format: OutputOptions) -> None:
    reader = PdfReader(str(pdf))
    # Links sometimes appear with duplicates /Rect,
    # so we skip duplicates and only display the 1st occurrence per (page, URI)
    links = {}
    for page_number, page in enumerate(reader.pages, start=1):
        if "/Annots" in page:
            page_annots: ArrayObject = page["/Annots"]  # type: ignore[assignment]
            for annot in page_annots:
                annotation = annot.get_object()
                if "/A" in annotation and "/URI" in annotation["/A"]:
                    # Extract hyperlink URL
                    uri = annotation["/A"]["/URI"]
                    # Extract bounding rectangle
                    rect = annotation.get("/Rect", "N/A")
                    link = UriLink(
                        uri=uri,
                        page=page_number,
                        rect=rect,
                    )
                    links[link.copy(update={"rect": []}).json()] = link

    if output_format == OutputOptions.json:
        print("[")
        for i, link in enumerate(links.values(), start=1):
            print("", link.json() + ("," if i < len(links) else ""))
        print("]")
    else:
        for link in links.values():
            print(f"Page {link.page}: {link.uri} - Rect: {link.rect}")
