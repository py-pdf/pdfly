"""Utilities and fixtures that are available automatically for all tests."""

import os
from pathlib import Path

from pdfly.cli import entry_point

TESTS_ROOT = Path(__file__).parent.resolve()
PROJECT_ROOT = TESTS_ROOT.parent
RESOURCES_ROOT = PROJECT_ROOT / "resources"


def run_cli(args):
    try:
        entry_point(args)
    except SystemExit as error:
        return error.code


try:
    from contextlib import chdir  # type: ignore
except ImportError:  # Fallback when not available (< Python 3.11):
    from contextlib import contextmanager

    @contextmanager
    def chdir(dir_path):
        """Non thread-safe context manager to change the current working directory."""
        cwd = Path.cwd()
        os.chdir(dir_path)
        try:
            yield
        finally:
            os.chdir(cwd)
