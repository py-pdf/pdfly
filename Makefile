maint:
	pre-commit autoupdate
	python -m pip install --upgrade .
	python -m pip lock --group dev --group docs .
	uv pip install -r pylock.toml
	git submodule update --remote

release:
	python make_release.py
	git commit -eF RELEASE_COMMIT_MSG.md

clean:
	find pdfly tests docs -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf Image9.png htmlcov docs/_build build dist dont_commit_merged.pdf dont_commit_writer.pdf pdfly.egg-info

lint:
	ruff format .
	ruff check --fix --unsafe-fixes .
	mypy pdfly/ tests/

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30
