"""
Unit tests for metadata module.
Tests the _format_permissions function and the meta CLI command.
"""

import json
from pathlib import Path

import pytest

from pdfly.metadata import _format_permissions
from .conftest import RESOURCES_ROOT, run_cli

SAMPLE_FILES = RESOURCES_ROOT / "sample-files"

# Optional: exercise the bitmask fallback with real pypdf flags if present
try:
    from pypdf.constants import UserAccessPermissions as UAP
except Exception:  # pragma: no cover
    UAP = None


class TestFormatPermissions:
    """Test the _format_permissions helper function."""

    def test_format_permissions_unencrypted(self):
        assert _format_permissions(None) == "n/a (unencrypted)"

    def test_format_permissions_encrypted_with_no_permissions(self, mocker):
        mock_uap = mocker.Mock()
        mock_uap.to_dict.return_value = {
            "PRINT": False,
            "PRINT_TO_REPRESENTATION": False,
            "MODIFY": False,
            "EXTRACT": False,
            "ADD_OR_MODIFY": False,
            "FILL_FORM_FIELDS": False,
            "EXTRACT_TEXT_AND_GRAPHICS": False,
            "ASSEMBLE_DOC": False,
        }
        assert _format_permissions(mock_uap) == "none (all denied)"

    def test_format_permissions_some_allowed_via_dict(self, mocker):
        mock_uap = mocker.Mock()
        # Order here controls output order
        mock_uap.to_dict.return_value = {
            "PRINT": True,
            "MODIFY": False,
            "EXTRACT": True,
            "ASSEMBLE_DOC": False,
        }
        formatted = _format_permissions(mock_uap)
        # Lower-case labels from label_map
        assert formatted == "print, extract"

    @pytest.mark.skipif(UAP is None, reason="pypdf flags not available")
    def test_format_permissions_some_allowed_bitmask_path(self):
        # Exercises the IntFlag/bitmask fallback (no to_dict)
        uap = UAP.PRINT | UAP.EXTRACT
        formatted = _format_permissions(uap)
        assert formatted == "print, extract"

    def test_format_permissions_unknown_when_unhandled_obj(self):
        class Weird:  # no to_dict, not int-castable
            pass
        assert _format_permissions(Weird()) == "unknown"


class TestMetaCommand:
    """End-to-end tests for the meta CLI command."""

    def test_meta_command_unencrypted_pdf(self, capsys):
        rel = Path("002-trivial-libre-office-writer/002-trivial-libre-office-writer.pdf")
        input_pdf = SAMPLE_FILES / rel
        if not input_pdf.exists():
            pytest.skip(f"Unencrypted PDF file not found: {input_pdf}")

        exit_code = run_cli(["meta", str(input_pdf), "--output", "json"])
        assert exit_code == 0

        captured = capsys.readouterr()
        metadata = json.loads(captured.out)
        assert metadata["permissions"] == "n/a (unencrypted)"
        # header fix: should read raw PDF header bytes as text
        assert metadata["pdf_file_version"].startswith("%PDF-")

    def test_meta_command_encrypted_pdf(self, capsys):
        rel = Path("005-libreoffice-writer-password/libreoffice-writer-password.pdf")
        input_pdf = SAMPLE_FILES / rel
        if not input_pdf.exists():
            pytest.skip(f"Encrypted PDF file not found: {input_pdf}")

        exit_code = run_cli(["meta", str(input_pdf), "--output", "json"])
        assert exit_code == 0

        captured = capsys.readouterr()
        metadata = json.loads(captured.out)

        assert "permissions" in metadata
        perms = metadata["permissions"]
        assert perms not in {"n/a (unencrypted)", "unknown"}
        # If not "all denied", check formatting invariants
        if perms != "none (all denied)":
            parts = [p.strip() for p in perms.split(",")]
            # lower-case labels
            assert all(p == p.lower() for p in parts)
            # only known labels
            allowed = {
                "print", "print-high", "modify", "extract",
                "annotate", "fill-forms", "accessibility-copy", "assemble",
            }
            assert set(parts).issubset(allowed)

        # header fix also applies on encrypted files
        assert metadata["pdf_file_version"].startswith("%PDF-")
