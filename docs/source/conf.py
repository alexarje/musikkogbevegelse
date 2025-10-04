import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('.'))

project = 'Musikk og bevegelse'
author = 'Alexander Refsum Jensenius'

extensions = [
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

# Prefer the sphinx-book-theme if available, otherwise fall back to RTD or alabaster
try:
    import sphinx_book_theme
    html_theme = 'sphinx_book_theme'
    html_theme_path = [sphinx_book_theme.get_html_theme_path()]
except Exception:
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except Exception:
        html_theme = 'alabaster'

html_static_path = ['_static']

# MyST options
myst_enable_extensions = [
    'colon_fence',
]

# -- Options for LaTeX output ---------------------------------------------
latex_engine = 'xelatex'
latex_elements = {
    # The paper size ('a4paper' or 'letterpaper')
    'papersize': 'a4paper',
    # Additional stuff for the LaTeX preamble
    'preamble': '\\usepackage{fontspec}\\setmainfont{DejaVu Serif}',
}

# Documents to build (source start file, target name, title, author, documentclass)
latex_documents = [
    ('index', 'MusikkOgBevegelse.tex', 'Musikk og bevegelse', 'ARJ', 'book'),
]
