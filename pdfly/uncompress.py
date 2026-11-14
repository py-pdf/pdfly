"""Module for uncompressing PDF content streams."""

from pathlib import Path

from pypdf import PdfWriter


def main(pdf: Path, output: Path) -> None:
    writer = PdfWriter(clone_from=pdf)

    for page in writer.pages:
        # get_contents() decodes all the filters of the content stream(s):
        contents = page.get_contents()
        if contents is not None:
            page.replace_contents(contents)

    with open(output, "wb") as fp:
        writer.write(fp)

    orig_size = pdf.stat().st_size
    uncomp_size = output.stat().st_size

    print(f"Original Size  : {orig_size:,}")
    print(
        f"Uncompressed Size: {uncomp_size:,} ({(uncomp_size / orig_size) * 100:.1f}% of original)"
    )
