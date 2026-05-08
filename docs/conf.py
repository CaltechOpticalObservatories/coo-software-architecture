import os, sys
from datetime import datetime
sys.path.insert(0, os.path.abspath("../src"))

project = "Instrument Control Software Architecture"
author = "Caltech Optical Observatories (COO) Software Team"
copyright = f"{datetime.now():%Y}, {author}"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]
autosummary_generate = True
autodoc_typehints = "description"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


templates_path = ["_templates"]
html_static_path = ["_static"]
html_theme = "shibuya"

# MyST Markdown
myst_enable_extensions = ["colon_fence", "deflist", "linkify"]
myst_fence_as_directive = ["mermaid"]
myst_heading_anchors = 3

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Mermaid diagrams
myst_fence_as_directive = ["mermaid"]
mermaid_output_format = "raw"

# Clean API index if empty (avoids warnings in fresh clones)
if not os.path.exists("api"):
    os.makedirs("api", exist_ok=True)

