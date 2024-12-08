maint:
	pre-commit autoupdate
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in
	pip-compile -U requirements/docs.in

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

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30

mutation-test:
	mutmut run

mutmut-results:
	mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut-results.xml
	junit2html mutmut-results.xml mutmut-results.html
