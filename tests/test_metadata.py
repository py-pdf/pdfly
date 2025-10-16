"""
Unit tests for metadata module.
Runs the meta CLI over every PDF in sample-files and checks permissions + header.
"""

import json
from pathlib import Path

import pytest

from .conftest import PROJECT_ROOT, run_cli  # provided by repo

SAMPLE_FILES = PROJECT_ROOT / "sample-files"
pytestmark = pytest.mark.skipif(
    not SAMPLE_FILES.exists(),
    reason="sample-files submodule not present",
)

PDFS = sorted(PROJECT_ROOT.rglob("*/*.pdf"))


def _expected_permissions_from_pdf(pdf_path: Path) -> str:
    """Compute expected permissions using pypdf, independent of the CLI."""
    try:
        from pypdf import PdfReader
        try:
            from pypdf.constants import UserAccessPermissions as UAP
        except Exception:
            UAP = None
    except Exception:
        # If pypdf isn't available for some reason, don't fail the test
        return "unknown"

    try:
        reader = PdfReader(str(pdf_path))
    except Exception:
        return "unknown"

    uap = getattr(reader, "user_access_permissions", None)
    if uap is None:
        return "n/a (unencrypted)"

    # Same labels as pdfly.metadata._format_permissions
    label_map = {
        "PRINT": "print",
        "PRINT_TO_REPRESENTATION": "print-high",
        "MODIFY": "modify",
        "EXTRACT": "extract",
        "ADD_OR_MODIFY": "annotate",
        "FILL_FORM_FIELDS": "fill-forms",
        "EXTRACT_TEXT_AND_GRAPHICS": "accessibility-copy",
        "ASSEMBLE_DOC": "assemble",
    }

    # Prefer to_dict() if available
    to_dict = getattr(uap, "to_dict", None)
    if callable(to_dict):
        try:
            flags = to_dict()
            items = [label_map.get(k, k.lower()) for k, v in flags.items() if v and k in label_map]
            return ", ".join(items) if items else "none (all denied)"
        except Exception:
            pass

    # Fallback: bitmask checks
    if UAP is not None:
        try:
            mask = int(uap)
            checks = [
                (UAP.PRINT, "print"),
                (UAP.PRINT_TO_REPRESENTATION, "print-high"),
                (UAP.MODIFY, "modify"),
                (UAP.EXTRACT, "extract"),
                (UAP.ADD_OR_MODIFY, "annotate"),
                (UAP.FILL_FORM_FIELDS, "fill-forms"),
                (UAP.EXTRACT_TEXT_AND_GRAPHICS, "accessibility-copy"),
                (UAP.ASSEMBLE_DOC, "assemble"),
            ]
            items = [label for flag, label in checks if (mask & int(flag)) != 0]
            return ", ".join(items) if items else "none (all denied)"
        except Exception:
            pass

    return "unknown"


@pytest.mark.parametrize(
    "input_pdf",
    PDFS,
    ids=lambda p: p.relative_to(SAMPLE_FILES).as_posix(),
)
def test_meta_command_on_all_sample_pdfs(input_pdf, capsys):
    # Run the CLI
    exit_code = run_cli(["meta", str(input_pdf), "--output", "json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    metadata = json.loads(captured.out)

    # Basic invariants / shape
    assert "pdf_file_version" in metadata
    assert metadata["pdf_file_version"].startswith("%PDF-")
    assert "permissions" in metadata

    # Compare permissions to what pypdf says
    actual = metadata["permissions"]
    expected = _expected_permissions_from_pdf(input_pdf)

    if expected in {"n/a (unencrypted)", "none (all denied)", "unknown"}:
        assert actual == expected
    else:
        act_set = {p.strip() for p in actual.split(",") if p.strip()}
        exp_set = {p.strip() for p in expected.split(",") if p.strip()}
        assert act_set == exp_set
