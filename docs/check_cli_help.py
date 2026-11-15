"""
Check that the `pdfly ... --help` output shown in the docs is up to date.

Every code block line of the form `$ pdfly ... --help` in README.md,
docs/index.rst and docs/user/*.md must be followed by the exact output of
that command. The terminal width of each block is taken from its widest
line, so that wide and narrow blocks can coexist. A `pdfly ... --help` line
without the `$ ` prompt counts as outdated.

Usage:
    uv run --frozen python docs/check_cli_help.py          # report
    uv run --frozen python docs/check_cli_help.py --fix    # rewrite

The output depends on the installed versions of typer and rich. Running it
with `uv run --frozen` uses the versions of uv.lock, as CI and pre-commit do.
"""

import argparse
import difflib
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WIDTH = 80
# The "$ " prompt is optional here, so that blocks which lack it are reported
# (and fixed) instead of being silently skipped
COMMAND_PATTERN = re.compile(
    r"^(?P<indent>\s*)(?:\$ )?pdfly(?P<args>(?: .*)?)$"
)
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

# Runs in a single subprocess, as importing pdfly takes about a second.
# Reads [[args, width], ...] from stdin and writes [[exit_code, stdout], ...]
RENDER_HELP = """
import contextlib, io, json, os, sys
from pdfly.cli import entry_point

results = []
for args, width in json.load(sys.stdin):
    os.environ["COLUMNS"] = str(width)  # read by rich for every new console
    stdout = io.StringIO()
    exit_code = 0
    with contextlib.redirect_stdout(stdout):
        try:
            entry_point(args=args, prog_name="pdfly")
        except SystemExit as exc:
            exit_code = exc.code if isinstance(exc.code, int) else 1
    results.append([exit_code, stdout.getvalue()])
json.dump(results, sys.stdout)
"""


@dataclass
class HelpBlock:
    path: Path
    args: list[str]
    indent: str
    command: str  # the command line, as it should be written
    start: int  # index of the command line
    end: int  # index after the last non-blank output line
    leading_blank: bool  # whether a blank line follows the command
    width: int

    @property
    def key(self) -> tuple[tuple[str, ...], int]:
        return tuple(self.args), self.width


def documentation_files() -> list[Path]:
    return [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs" / "index.rst",
        *sorted((REPO_ROOT / "docs" / "user").glob("*.md")),
    ]


def find_help_blocks(path: Path, lines: list[str]) -> list[HelpBlock]:
    blocks = []
    for i, line in enumerate(lines):
        match = COMMAND_PATTERN.match(line)
        if match is None:
            continue
        args = shlex.split(match["args"])
        if "--help" not in args:
            continue
        indent = match["indent"]
        end = i + 1
        while end < len(lines) and not is_block_end(path, lines[end], indent):
            end += 1
        while end > i + 1 and not lines[end - 1].strip():
            end -= 1
        output = lines[i + 1 : end]
        leading_blank = bool(output) and not output[0].strip()
        width = max(
            (len(line) - len(indent) for line in output),
            default=DEFAULT_WIDTH,
        )
        blocks.append(
            HelpBlock(
                path=path,
                args=args,
                indent=indent,
                command=f"{indent}$ pdfly{match['args'].rstrip()}",
                start=i,
                end=end,
                leading_blank=leading_blank,
                width=width,
            )
        )
    return blocks


def is_block_end(path: Path, line: str, indent: str) -> bool:
    if path.suffix == ".md":
        return line.strip().startswith("```")
    # reStructuredText: the code block ends with the first line which is
    # indented less than its content
    return bool(line.strip()) and not line.startswith(indent)


def render_help(
    requests: list[tuple[tuple[str, ...], int]],
) -> dict[tuple[tuple[str, ...], int], list[str]]:
    """Return the output lines of `pdfly *args` for each (args, width)."""
    env = {
        key: value
        for key, value in os.environ.items()
        # typer enables colors in GitHub Actions or when asked to, and
        # TERMINAL_WIDTH would override the width of every block
        if key
        not in {"GITHUB_ACTIONS", "FORCE_COLOR", "PY_COLORS", "TERMINAL_WIDTH"}
    }
    env.update(
        {
            "NO_COLOR": "1",
            "TERM": "dumb",
            "_TYPER_FORCE_DISABLE_TERMINAL": "1",
            "PYTHONIOENCODING": "utf-8",
        }
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", RENDER_HELP],
        input=json.dumps([[list(args), width] for args, width in requests]),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        cwd=REPO_ROOT,  # document the pdfly of this checkout
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Rendering the help failed:\n{result.stderr}")

    rendered = {}
    for (args, width), (exit_code, stdout) in zip(
        requests, json.loads(result.stdout), strict=True
    ):
        if exit_code != 0:
            raise RuntimeError(
                f"'pdfly {shlex.join(args)}' failed with exit code "
                f"{exit_code}:\n{result.stderr}"
            )
        output = [
            ANSI_ESCAPE.sub("", line).rstrip() for line in stdout.splitlines()
        ]
        while output and not output[0]:
            output.pop(0)
        while output and not output[-1]:
            output.pop()
        rendered[args, width] = output
    return rendered


def expected_lines(block: HelpBlock, output: list[str]) -> list[str]:
    if block.leading_blank:
        output = ["", *output]
    return [
        block.command,
        *(block.indent + line if line else "" for line in output),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--fix", action="store_true", help="rewrite outdated blocks"
    )
    args = parser.parse_args()

    files = {}
    for path in documentation_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        files[path] = (lines, find_help_blocks(path, lines))
    requests = list(
        dict.fromkeys(
            block.key for _, blocks in files.values() for block in blocks
        )
    )
    try:
        rendered = render_help(requests)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 2

    outdated = 0
    for path, (lines, blocks) in files.items():
        changed = False
        # Process from the bottom, so that replacing a block does not shift
        # the line numbers of the blocks above it
        for block in reversed(blocks):
            actual = lines[block.start : block.end]
            expected = expected_lines(block, rendered[block.key])
            if actual == expected:
                continue
            outdated += 1
            changed = True
            diff = difflib.unified_diff(
                actual,
                expected,
                fromfile=f"{path.relative_to(REPO_ROOT)}:{block.start + 1}",
                tofile=f"pdfly {shlex.join(block.args)}",
                lineterm="",
            )
            print("\n".join(diff), end="\n\n")
            lines[block.start : block.end] = expected
        if args.fix and changed:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if outdated == 0:
        print("The documented CLI help is up to date.")
        return 0
    if args.fix:
        print(f"Updated {outdated} outdated help block(s).")
        return 0
    print(
        f"{outdated} help block(s) are outdated. Run "
        "'uv run --frozen python docs/check_cli_help.py --fix' to update them."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
