# CHANGELOG

## Unreleased

### Bug Fixes (BUG)
- Correct the command descriptions and example in 2-up and uncompress help (#289)

## Version 0.6.0, 2026-11-14

### Deprecations (DEP)
- Drop Python 3.10 (#293)

### New Features (ENH)
- New decrypt command (#298)
- Allow to specify a page range in extract-images (#284)
- New command extract-links (#271)
- pagemeta now displays the name of a known page format that is close to the page dimensions (#222)
- extract-images: Format output filenames with four digit page numbers to make output alphabetical (#197)

### Bug Fixes (BUG)
- Fix uncompress and meta, and require 100% test coverage (#294)
- Write to stdout when `pdfly cat` has no `-o` option (#290)
- Support pypdf 7 in booklet, up2 and sign (#291)
- fix some edge case in extract-links (#272)
- Fix #218 - 2up incorrectly handle documents with an odd number of pages (#219)

### Documentation (DOC)
- Fix typos in comments, docstrings and a local variable name (#277)
- Added documentation & unit tests for: pdfly cat --password (#212)
- Minor documentation improvement (#203)
- Various minor edits (#188)

### Developer Experience (DEV)
- Run mypy in strict mode (#299)
- Coverage measurement only on the latest ubuntu (#295)
- Add ci-success step in github-ci workflow (#279)

### Maintenance (MAINT)
- Update crate-ci/typos action to v1.52.2 (#285)
- Modernize repository tooling and CI (#281)
- Update actions/setup-python action to v7.1.0 (#276)
- Update softprops/action-gh-release digest to efb3536 (#274)
- Update crate-ci/typos action to v1.51.1 (#273)
- Update crate-ci/typos action to v1.49.0 (#270)
- Update actions/checkout action to v7.0.1 (#267)
- Update actions/setup-python action to v7 (#266)
- Update softprops/action-gh-release digest to 3d0d988 (#265)
- Update crate-ci/typos action to v1.48.0 (#264)
- Update actions/cache action to v6.1.0 (#263)
- Update actions/cache action to v6 (#261)
- Update actions/setup-python action to v6.3.0 (#262)
- Update softprops/action-gh-release digest to 718ea10 (#260)
- Update actions/checkout action to v7 (#259)
- Update crate-ci/typos action to v1.47.2 (#258)
- Update actions/checkout action to v6.0.3 (#257)
- Update crate-ci/typos action to v1.47.1 (#256)
- Update crate-ci/typos action to v1.46.3 (#255)
- Update crate-ci/typos action to v1.46.2 (#254)
- Update crate-ci/typos action to v1.46.1 (#253)
- Update crate-ci/typos action to v1.45.2 (#252)
- Update actions/cache action to v5.0.5 (#250)
- Update crate-ci/typos action to v1.45.1 (#251)
- Update softprops/action-gh-release action to v3 (#249)
- Update crate-ci/typos action to v1.45.0 (#246)
- Update actions/cache action to v5.0.4 (#245)
- Update dependencies (#244)
- Update crate-ci/typos action to v1.44.0 (#242)
- Update softprops/action-gh-release action to v2.6.1 (#243)
- Update crate-ci/typos action to v1.43.5 (#240)
- Update crate-ci/typos action to v1.43.4 (#239)
- Update crate-ci/typos action to v1.43.3 (#238)
- Update crate-ci/typos action to v1.43.2 (#237)
- Update crate-ci/typos action to v1.43.1 (#236)
- Update actions/cache action to v5.0.3 (#234)
- Update crate-ci/typos action to v1.42.3 (#233)
- Update crate-ci/typos action to v1.42.2 (#232)
- Update actions/checkout action to v6.0.2 (#231)
- Update actions/setup-python action to v6.2.0 (#230)
- Update crate-ci/typos action to v1.42.1 (#228)
- Update actions/cache action to v5.0.2 (#227)
- Ensure Windows support - fix #224 (#225)
- Update crate-ci/typos action to v1.42.0 (#223)
- Update crate-ci/typos action to v1.41.0 (#221)
- Update actions/cache action to v5.0.1 (#217)
- Update actions/cache action to v5 (#216)
- Update actions/checkout action to v6.0.1 (#214)
- Update softprops/action-gh-release action to v2.5.0 (#211)
- Update crate-ci/typos action to v1.40.0 (#210)
- Update actions/setup-python action to v6.1.0 (#209)
- Update actions/checkout action to v6 (#208)
- Update actions/checkout action to v5.0.1 (#207)
- Update crate-ci/typos action to v1.39.2 (#206)
- Update crate-ci/typos action to v1.39.1 (#205)
- Ensured support for Python 3.14 (#204)
- Minor edits (#201)
- Update softprops/action-gh-release action to v2.4.2 (#198)
- Update crate-ci/typos action to v1.39.0 (#196)

### Other
- Docs: Add lkintact as a contributor for bug (#220)
- Docs: Add georgthegreat as a contributor for code (#202)
- Docs: Add georgthegreat as a contributor for ideas (#192)
- Docs: minor improvements (#187)

[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.5.1...0.6.0)

## Version 0.6.0, not released yet

### Bug Fixes (BUG)
- `2up` incorrectly handled documents with an odd number of pages - [issue #219](https://github.com/py-pdf/pdfly/issues/218)

### New Features (ENH)
- New `decrypt` command, removing password protection from an encrypted PDF - [issue #275](https://github.com/py-pdf/pdfly/issues/275)
- New `extract-links` command ([PR #271](https://github.com/py-pdf/pdfly/pull/271))
- `pagemeta` now displays the name of a known page format that is close to the page dimensions
- `extract-images` now accepts an optional page range, to only extract images from specific pages - [issue #194](https://github.com/py-pdf/pdfly/issues/194)
- ensured support for Python 3.15

### Deprecations (DEP)
- support for Python 3.10 has been dropped, as it reached its end of life on 2026-10-01: `pdfly` now requires Python 3.11+

### Maintenance (MAINT)
- `check-sign` and `sign` now use endesive 3, which no longer depends on oscrypto


### Developer Experience (DEV)
- mypy now runs in strict mode


## Version 0.5.1, 2025-10-13

### New Features (ENH)
- `extract-images`: output filenames are now formatted using four digit for page numbers, in order for output files to be ordered alphabetically
- ensured support for Python 3.14

### Bug Fixes (BUG)
- `requests` is now a dependency, to prevent a `ModuleNotFoundError` when running with `uv`


## Version 0.5.0, 2025-10-13

### New Features (ENH)
- New `extract-annotated-pages` to filter out only the user annotated pages ([PR #98](https://github.com/py-pdf/pdfly/pull/98))
- New `rotate` sub-command to rotate specified pages ([PR #128](https://github.com/py-pdf/pdfly/pull/128))
- Added optional `--password` argument to `cat` to perform decryption ([PR #61](https://github.com/py-pdf/pdfly/pull/61))
- `pagemeta` now displays known page formats when it can detect it: A3, A4, A5, Letter, Legal
- `pagemeta` now displays the rotation value.
- New `sign` sub-command to create a signed pdf from an existing pdf ([PR #165](https://github.com/py-pdf/pdfly/pull/165))
- New `check-sign` sub-command to verify the signature of a signed pdf ([PR #166](https://github.com/py-pdf/pdfly/pull/166))

### Bug Fixes (BUG)
- `pypdf[full]` is now a dependency, instead of just `pypdf`, to avoid some cases of `DependencyError`

### Deprecations (DEP)
* support for older Python3 versions has been dropped, `pdfly` now requires Python 3.10+


## Version 0.4.0, 2024-12-08

### New Features (ENH)
- New `booklet` command to adjust offsets and lengths ([PR #77](https://github.com/py-pdf/pdfly/pull/77))
- New `uncompress` command ([PR #75](https://github.com/py-pdf/pdfly/pull/75))
- New `update-offsets` command to adjust offsets and lengths ([PR #15](https://github.com/py-pdf/pdfly/pull/15))
- New `rm` command ([PR #59](https://github.com/py-pdf/pdfly/pull/59))
- `metadata`: now also displaying CreationDate, Creator, Keywords & Subject ([PR #73](https://github.com/py-pdf/pdfly/pull/73))
- Add warning for out-of-bounds page range in pdfly `cat` command ([PR #58](https://github.com/py-pdf/pdfly/pull/58))

### Bug Fixes (BUG)
- `2-up` command, that only showed one page per sheet, on the left side, with blank space on the right ([PR #78](https://github.com/py-pdf/pdfly/pull/78))

[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.3.3...0.4.0)


## Version 0.3.3, 2024-04-14

### Developer Experience (DEV)
-  Chain workflows

[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.3.2...0.3.3)


## Version 0.3.2, 2024-04-14

### Developer Experience (DEV)
-  Decouple git tag / PyPI release / Github release page (#49, #50)


[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.3.1...0.3.2)

## Version 0.3.1, 2024-03-29

### Maintenance (MAINT)
-  Update pypdf usage (#48)

### Developer Experience (DEV)
-  Release via REL commit (#48)
-  Fix mypy issues
-  Add make_release.py

[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.3.0...0.3.1)

## Version 0.3.0, 2023-12-17

### New Features (ENH)
-  Add x2pdf command (#25)

### Bug Fixes (BUG)
-  boxes are floats, not int
-  Add missing fpdf2 dependency (#29)

### Documentation (DOC)
-  cat command
-  More examples for the cat subcommand
-  Add cat subcommand
-  Link to readthedocs
-  Add project governance file
-  Move readthedocs config file to root
-  Add docs (#24)

### Developer Experience (DEV)
-  Checkout sample-files in CI (#30)
-  Let dependabot update Github Actions
-  Add action for automatic releases

### Maintenance (MAINT)
-  Update dependencies (#42)
-  In the cat subcommand, replace the usage of the deprecated PdfMerger by PdfWriter (#34)
-  Update .pre-commit-config.yaml
-  Adjust x2pdf syntax

### Testing (TST)
-  cat with two files (#41)
-  Test cat command with more parameters + validate result (#40)
-  Adding unit tests (#28)

### Other
- : [{'msg': 'Bump actions/setup-python from 4 to 5 (#39)', 'author': 'dependabot[bot]'}, {'msg': 'test_extract_images_monochrome() is now passing', 'author': 'CimonLucas(LCM)'}, {'msg': 'Bump actions/setup-python from 3 to 4 (#27)', 'author': 'dependabot[bot]'}, {'msg': 'Bump actions/checkout from 3 to 4 (#26)', 'author': 'dependabot[bot]'}, {'msg': 'Ensure input PDF exists for cat subcommand', 'author': 'MartinThoma'}]

[Full Changelog](https://github.com/py-pdf/pdfly/compare/0.2.14...0.3.0)
