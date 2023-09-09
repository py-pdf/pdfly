"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options.
For a full list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import shutil
import sys

import pdfly as py_pkg

sys.path.insert(0, os.path.abspath("."))  # noqa
sys.path.insert(0, os.path.abspath("../"))  # noqa

shutil.copyfile("../CHANGELOG.md", "meta/CHANGELOG.md")
shutil.copyfile("../CONTRIBUTORS.md", "meta/CONTRIBUTORS.md")

# -- Project information -----------------------------------------------------

project = py_pkg.__name__
copyright = "2023, pdfly contributors"
author = "pdfly contributors"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = py_pkg.__version__
# The full version, including alpha/beta/rc tags.
release = py_pkg.__version__

# -- General configuration ---------------------------------------------------
# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "4.0.0"

myst_all_links_external = True
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    # External
    "myst_parser",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
}

nitpick_ignore_regex = [
    # For reasons unclear at this stage the io module prefixes everything with _io
    # and this confuses sphinx
    (r"py:class", r"_io.(FileIO|BytesIO|Buffered(Reader|Writer))"),
]

autodoc_default_options = {
    "member-order": "bysource",
    "members": True,
    "show-inheritance": True,
    "undoc-members": True,
}
autodoc_inherit_docstrings = False
autodoc_typehints_format = "short"
python_use_unqualified_type_names = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": True,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for Napoleon  -----------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False  # Explicitly prefer Google style docstring
napoleon_use_param = True  # for type hint support
napoleon_use_rtype = (
    False  # False so the return type is inline with the description.
)
