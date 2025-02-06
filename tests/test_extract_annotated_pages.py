from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_annotated_pages_input8(capsys, tmp_path):
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(RESOURCES_ROOT / "input8.pdf"),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 pages with annotations" in captured.out
