"""Sphinx configuration for the result documentation."""

from importlib import metadata

project = "result"
author = "Danilo Bargen and contributors"
copyright = "Danilo Bargen and contributors"
release = metadata.version("result")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# Docstrings use single backticks for inline code
default_role = "code"

autodoc_member_order = "bysource"
autodoc_default_options = {"members": True}

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# Let the README's `[text](#heading)` links resolve when it is included
myst_heading_anchors = 3

exclude_patterns = ["_build"]

html_theme = "furo"
html_title = "result"
html_baseurl = "https://john-parton.github.io/result/"
