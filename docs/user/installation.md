# Installation
There are several ways to install pdfly. The most common option is to use pip.

## pip
pdfly requires Python 3.10+ to run.

Typically Python comes with `pip`, a package installer. Using it you can
install pdfly:

```bash
pip install pdfly
```

If you are not a super-user (a system administrator / root), you can also just
install pdfly for your current user:

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

## uv
pdfly can be run without persistent installation using [uv tool run](https://docs.astral.sh/uv/guides/tools/#running-tools):

```bash
uv tool run pdfly 
```

via the [uvx](https://docs.astral.sh/uv/guides/tools/#running-tools) alias: 

```bash
uvx pdfly
```

or it can be installed using [uv tool install](https://docs.astral.sh/uv/guides/tools/#installing-tools):

```bash
uv tool install pdfly
```

## Python Version Support
If ✓ is given, it works. It is tested via CI.
If ✖ is given, it is guaranteed not to work.
If it's not filled, we don't guarantee support, but it might still work.


| Python                 | 3.13 | 3.12 | 3.11 | 3.10 | 2.7 |
| ---------------------- | ---- | ---- | ---- | ---- | --- |
| pdfly                  |  ✓   |  ✓  |  ✓   |  ✓   |  ✖  |


## Development Version
In case you want to use the current version under development:

```bash
pip install git+https://github.com/py-pdf/pdfly.git
```
