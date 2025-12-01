from pathlib import Path
from typing import Any

import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def extract_embedded_images(pdf_filepath: Path) -> list[Any]:
    reader = PdfReader(pdf_filepath)
    return [page.images for page in reader.pages]


def extract_text_pages(pdf_filepath: Path) -> list[str]:
    reader = PdfReader(pdf_filepath)
    return [page.extract_text() for page in reader.pages]


def test_cat_incorrect_number_of_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(["cat", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing" in captured.err


def test_cat_two_files_ok(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "box.pdf"),
                str(RESOURCES_ROOT / "jpeg.pdf"),
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0, captured
    assert not captured.err
    reader = PdfReader(tmp_path / "out.pdf")
    assert len(reader.pages) == 2


def test_cat_subset_ok(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
                "13:15",
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    reader = PdfReader(tmp_path / "out.pdf")
    assert len(reader.pages) == 2


@pytest.mark.parametrize(
    "page_range",
    ["a", "-", "1-", "1-1-1", "1:1:1:1"],
)
def test_cat_subset_invalid_args(
    capsys: pytest.CaptureFixture, tmp_path: Path, page_range: str
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "jpeg.pdf"),
                page_range,
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 2, captured
    assert "Error: invalid file path or page range provided" in captured.out


def test_cat_subset_warn_on_missing_pages(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "jpeg.pdf"),
                "2",
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert "WARN" in captured.err


def test_cat_subset_ensure_reduced_size(
    tmp_path: Path, two_pages_pdf_filepath: Path
) -> None:
    exit_code = run_cli(
        [
            "cat",
            str(two_pages_pdf_filepath),
            "0",
            "--output",
            str(tmp_path / "page1.pdf"),
        ]
    )
    assert exit_code == 0
    # The extracted PDF should only contain ONE image:
    embedded_images = extract_embedded_images(tmp_path / "page1.pdf")
    assert len(embedded_images) == 1

    exit_code = run_cli(
        [
            "cat",
            str(two_pages_pdf_filepath),
            "1",
            "--output",
            str(tmp_path / "page2.pdf"),
        ]
    )
    assert exit_code == 0
    # The extracted PDF should only contain ONE image:
    embedded_images = extract_embedded_images(tmp_path / "page2.pdf")
    assert len(embedded_images) == 1


def test_cat_combine_files(
    pdf_file_100: Path,
    pdf_file_abc: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    with chdir(tmp_path):
        output_pdf_path = tmp_path / "out.pdf"

        # Run pdfly cat command
        exit_code = run_cli(
            [
                "cat",
                str(pdf_file_100),
                "1:10:2",
                str(pdf_file_abc),
                "::2",
                str(pdf_file_abc),
                "1::2",
                "--output",
                str(output_pdf_path),
            ]
        )
        captured = capsys.readouterr()

        # Check if the command was successful
        assert exit_code == 0, captured.out

        # Extract text from the original and modified PDFs
        extracted_pages = extract_text_pages(output_pdf_path)

        # Compare the extracted text
        assert extracted_pages == [
            "1",
            "3",
            "5",
            "7",
            "9",
            "a",
            "c",
            "e",
            "g",
            "i",
            "k",
            "m",
            "o",
            "q",
            "s",
            "u",
            "w",
            "y",
            "b",
            "d",
            "f",
            "h",
            "j",
            "l",
            "n",
            "p",
            "r",
            "t",
            "v",
            "x",
            "z",
        ]


@pytest.mark.parametrize(
    ("page_range", "expected"),
    [
        ("22", ["22"]),
        ("0:3", ["0", "1", "2"]),
        (":3", ["0", "1", "2"]),
        (":", [str(el) for el in range(100)]),
        ("5:", [str(el) for el in list(range(100))[5:]]),
        ("::2", [str(el) for el in list(range(100))[::2]]),
        ("1:10:2", [str(el) for el in list(range(100))[1:10:2]]),
        ("::1", [str(el) for el in list(range(100))[::1]]),
        ("::-1", [str(el) for el in list(range(100))[::-1]]),
    ],
)
def test_cat_commands(
    pdf_file_100: Path,
    tmp_path: Path,
    page_range: str,
    expected: list[str],
) -> None:
    with chdir(tmp_path):
        output_pdf_path = tmp_path / "out.pdf"

        # Run pdfly cat command
        exit_code = run_cli(
            [
                "cat",
                str(pdf_file_100),
                page_range,
                "--output",
                str(output_pdf_path),
            ]
        )

        # Check if the command was successful
        assert exit_code == 0

        # Extract text from the original and modified PDFs
        extracted_pages = extract_text_pages(output_pdf_path)

        # Compare the extracted text
        assert extracted_pages == expected


def test_cat_decrypt_with_password_ok(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    exit_code = run_cli(
        [
            "cat",
            "--password=openpassword",
            "sample-files/005-libreoffice-writer-password/libreoffice-writer-password.pdf",
            "--output",
            str(tmp_path / "out.pdf"),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    reader = PdfReader(tmp_path / "out.pdf")
    assert len(reader.pages) == 1


def test_cat_decrypt_with_password_ko(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    exit_code = run_cli(
        [
            "cat",
            "--password=INCORRECT",
            "sample-files/005-libreoffice-writer-password/libreoffice-writer-password.pdf",
            "--output",
            str(tmp_path / "out.pdf"),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1, captured
    assert "Error: the decrypting password provided is invalid" in captured.out
