# Installation

There are several ways to install pdfly. The most common option is to use pip.

## pip

pdfly requires Python 3.6+ to run.

Typically Python comes with `pip`, a package installer. Using it you can
install pypdf:

```bash
pip install pdfly
```

If you are not a super-user (a system administrator / root), you can also just
install pypdf for your current user:

```bash
pip install --user pdfly
```

## pipx

We recommend to install pdfly via [pipx](https://pypi.org/project/pipx/):

```bash
pipx install pdfly
```

pipx installs the pdfly application in an isolated environment. That guarantees
that no other applications interferes with its defpendencies.

## Python Version Support

If ✓ is givien, it works. It is tested via CI.
If ✖ is given, it is guaranteed not to work.
If it's not filled, we don't guarantee support, but it might still work.


| Python                 | 3.12 | 3.11 | 3.10 | 3.9 | 3.8 | 3.7 | 3.6 | 2.7 |
| ---------------------- | ---- | ---- | ---- | --- | --- | --- | --- | --- |
| pdfly                  |  ✓   |  ✓   |  ✓   |  ✓  |  ✓  |     |     |  ✖  |


## Development Version

In case you want to use the current version under development:

```bash
pip install git+https://github.com/py-pdf/pdfly.git
```
