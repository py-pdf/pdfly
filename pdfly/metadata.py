"""Show metadata of a PDF file"""

import stat
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pypdf import PdfReader

from ._utils import OutputOptions


class EncryptionData(BaseModel):
    revision: int
    v_value: int


class MetaInfo(BaseModel):
    encryption: Optional[EncryptionData] = None
    pdf_file_version: str
    pages: Optional[int] = None
    page_mode: Optional[str] = None
    page_layout: Optional[str] = None
    attachments: str = "unknown"
    id1: Optional[bytes] = None
    id2: Optional[bytes] = None
    images: list[int] = []

    # PDF /Info dictionary
    author: Optional[str] = None
    creation_date: Optional[datetime] = None
    creator: Optional[str] = None
    keywords: Optional[str] = None
    producer: Optional[str] = None
    subject: Optional[str] = None
    title: Optional[str] = None

    # OS Information
    file_permissions: str
    file_size: int  # in bytes
    creation_time: datetime
    modification_time: datetime
    access_time: datetime


def main(pdf: Path, output: OutputOptions) -> None:
    reader = PdfReader(str(pdf))
    if reader.is_encrypted:
        pdf_stat = pdf.stat()
        meta = MetaInfo(
            encryption=(
                EncryptionData(
                    v_value=reader._encryption.V,
                    revision=reader._encryption.R,
                )
                if reader.is_encrypted and reader._encryption
                else None
            ),
            pdf_file_version=reader.stream.read(8).decode("utf-8"),
            # OS Info
            file_permissions=f"{stat.filemode(pdf_stat.st_mode)}",
            file_size=pdf_stat.st_size,
            creation_time=datetime.fromtimestamp(pdf_stat.st_ctime),
            modification_time=datetime.fromtimestamp(pdf_stat.st_mtime),
            access_time=datetime.fromtimestamp(pdf_stat.st_atime),
        )
    else:
        info = reader.metadata

        reader.stream.seek(0)
        pdf_file_version = reader.stream.read(8).decode("utf-8")
        pdf_stat = pdf.stat()
        pdf_id = reader.trailer.get("/ID")
        meta = MetaInfo(
            pages=len(reader.pages),
            encryption=(
                EncryptionData(
                    v_value=reader._encryption.V,  # type: ignore
                    revision=reader._encryption.R,  # type: ignore
                )
                if reader.is_encrypted and reader._encryption
                else None
            ),
            page_mode=reader.page_mode,
            pdf_file_version=pdf_file_version,
            page_layout=reader.page_layout,
            attachments=str(list(reader.attachments.keys())),
            id1=pdf_id[0] if pdf_id is not None else None,
            id2=pdf_id[1] if pdf_id is not None and len(pdf_id) >= 2 else None,
            # OS Info
            file_permissions=f"{stat.filemode(pdf_stat.st_mode)}",
            file_size=pdf_stat.st_size,
            creation_time=datetime.fromtimestamp(pdf_stat.st_ctime),
            modification_time=datetime.fromtimestamp(pdf_stat.st_mtime),
            access_time=datetime.fromtimestamp(pdf_stat.st_atime),
            images=[
                len(image.data)
                for page in reader.pages
                for image in page.images
            ],
        )
        if info is not None:
            meta.author = info.author
            meta.creation_date = info.creation_date
            meta.creator = info.creator
            # Pending https://github.com/py-pdf/pypdf/pull/2939 to be able to access .keywords:
            meta.keywords = info.get("/Keywords")
            meta.producer = info.producer
            meta.subject = info.subject
            meta.title = info.title

    if output == OutputOptions.json:
        print(meta.json())
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table(title="PDF Data")
        table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        table.add_column("Value", style="white")

        if meta.title:
            table.add_row("Title", meta.title)
        if meta.author:
            table.add_row("Author", meta.author)
        if meta.creation_date:
            table.add_row("CreationDate", str(meta.creation_date))
        if meta.creator:
            table.add_row("Creator", meta.creator)
        if meta.producer:
            table.add_row("Producer", meta.producer)
        if meta.subject:
            table.add_row("Subject", meta.subject)
        if meta.keywords:
            table.add_row("Keywords", meta.keywords)
        table.add_row("Pages", f"{meta.pages:,}" if meta.pages else "unknown")
        table.add_row("Encrypted", f"{meta.encryption}")
        table.add_row("PDF File Version", meta.pdf_file_version)
        table.add_row("Page Layout", meta.page_layout)
        table.add_row("Page Mode", meta.page_mode)
        table.add_row("PDF ID", f"ID1={meta.id1!r} ID2={meta.id2!r}")
        embedded_fonts: set[str] = set()
        unemedded_fonts: set[str] = set()
        if not reader.is_encrypted:
            for page in reader.pages:
                emb, unemb = page._get_fonts()
                embedded_fonts = embedded_fonts.union(set(emb))
                unemedded_fonts = unemedded_fonts.union(set(unemb))
            table.add_row(
                "Fonts (unembedded)", ", ".join(sorted(unemedded_fonts))
            )
            table.add_row(
                "Fonts (embedded)", ", ".join(sorted(embedded_fonts))
            )
        table.add_row("Attachments", meta.attachments)
        table.add_row(
            "Images", f"{len(meta.images)} images ({sum(meta.images):,} bytes)"
        )

        enc_table = Table(title="Encryption information")
        enc_table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        enc_table.add_column("Value", style="white")
        if meta.encryption:
            enc_table.add_row(
                "Security Handler Revision Number",
                str(meta.encryption.revision),
            )
            enc_table.add_row("V value", str(meta.encryption.v_value))

        os_table = Table(title="Operating System Data")
        os_table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        os_table.add_column("Value", style="white")
        os_table.add_row("File Name", f"{pdf}")
        os_table.add_row("File Permissions", f"{meta.file_permissions}")
        os_table.add_row("File Size", f"{meta.file_size:,} bytes")
        os_table.add_row(
            "Creation Time", f"{meta.creation_time:%Y-%m-%d %H:%M:%S}"
        )
        os_table.add_row(
            "Modification Time", f"{meta.modification_time:%Y-%m-%d %H:%M:%S}"
        )
        os_table.add_row(
            "Access Time", f"{meta.access_time:%Y-%m-%d %H:%M:%S}"
        )

        console = Console()
        console.print(os_table)
        console.print(table)
        if meta.encryption:
            console.print(enc_table)
        console.print(
            "Use the 'pagemeta' subcommand to get details about a single page"
        )
