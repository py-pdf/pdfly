maint:
	pre-commit autoupdate
	python -m pip install --upgrade .
	python -m pip lock --group dev --group docs .
	uv pip install -r pylock.toml

release:
	python make_release.py
	git commit -eF RELEASE_COMMIT_MSG.md

upload:
	make clean
	flit publish

clean:
	python setup.py clean --all
	pyclean .
	rm -rf tests/__pycache__ pdfly/__pycache__ Image9.png htmlcov docs/_build dist dont_commit_merged.pdf dont_commit_writer.pdf pdfly.egg-info

lint:
	mypy . --ignore-missing-imports --exclude build
	ruff check --fix --unsafe-fixes

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30
