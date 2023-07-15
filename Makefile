maint:
	pre-commit autoupdate
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

upload:
	make clean
	flit publish

clean:
	python setup.py clean --all
	pyclean .
	rm -rf Tests/__pycache__ pypdf/__pycache__ Image9.png htmlcov docs/_build dist dont_commit_merged.pdf dont_commit_writer.pdf pypdf.egg-info pypdf_pdfLocation.txt

test:
	pytest Tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30

mutation-test:
	mutmut run

mutmut-results:
	mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut-results.xml
	junit2html mutmut-results.xml mutmut-results.html
