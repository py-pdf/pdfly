"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_update_offsets(capsys, tmp_path: Path) -> None:
    # Arrange
    input = str(RESOURCES_ROOT / "hello.pdf")
    file_expected = str(RESOURCES_ROOT / "hello-expected.pdf")
    output = tmp_path / "hello-out.pdf"
    assert not output.exists()

    # Act
    exit_code = run_cli(
        [
            "update-offsets",
            str(input),
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    assert f"Wrote {output}" in captured.out
    assert output.exists()
    with open(file_expected, 'r', encoding='iso-8859-1') as file_exp:
        lines_exp = file_exp.readlines()
    with open(output, 'r', encoding='iso-8859-1') as file_act:
        lines_act = file_act.readlines()
    assert len(lines_exp) == len(lines_act), f"lines_exp=f{lines_exp}, lines_act=f{lines_act}"
    for line_no, (line_exp, line_act) in enumerate(zip(lines_exp, lines_act), start = 1):
        assert line_exp == line_act, f"Lines differ in line {line_no}"

