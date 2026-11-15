SHELL := /bin/bash

maint:
	pre-commit autoupdate
	python -m pip install --upgrade .
	# Universal lock: valid on every platform and Python version pdfly supports
	uv pip compile pyproject.toml --group dev --group docs --universal --python-version 3.11 -o pylock.toml
	uv pip install -r pylock.toml
	git submodule update --remote

# Step 1 of a release: bump version, update CHANGELOG, write the commit message.
# The publishing itself is done by GitHub Actions, see docs/dev/release.md
prepare-release:
	python make_release.py

# Manual fallback for publishing, only for when GitHub Actions is not working.
# The normal path is to merge the "REL: X.Y.Z" PR, see docs/dev/release.md
release:
	@echo "WARNING: This publishes to PyPI from your machine. This cannot be undone."
	@echo "The normal path is to merge the REL pull request and let GitHub publish."
	@read -r -p "Do you really want to do this? [y/N] " answer; \
		[ "$$answer" = "y" ] || { echo "Aborted."; exit 1; }
	@test -z "$$(git status --porcelain)" || { echo "Working tree is not clean."; exit 1; }
	@version=$$(uv version --short 2>/dev/null); \
		git log -1 --format=%s | grep -q "^REL: $$version\b" || { echo "HEAD is not the 'REL: $$version' commit. Run 'make prepare-release' and commit first."; exit 1; }
	rm -rf ./dist
	uv build
	uv publish

clean:
	find pdfly tests docs -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf Image9.png htmlcov docs/_build build dist dont_commit_merged.pdf dont_commit_writer.pdf pdfly.egg-info

lint:
	ruff format .
	ruff check --fix --unsafe-fixes .
	mypy pdfly/ tests/

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30
