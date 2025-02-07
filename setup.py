"""Package pdfly with setuptools."""

import re

from setuptools import find_packages, setup

VERSIONFILE = "pdfly/_version.py"
with open(VERSIONFILE) as fp:
    verstrline = fp.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.MULTILINE)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    version=verstr,
    packages=find_packages(exclude=("tests",)),
)
