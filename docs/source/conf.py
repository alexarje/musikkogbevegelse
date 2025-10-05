import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('.'))

project = 'Musikk og bevegelse'
author = 'Alexander Refsum Jensenius'

# Set explicit HTML titles so theme doesn't append 'documentation'
html_title = project
html_short_title = project

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

# If a LaTeX-generated PDF exists (from a prior latexpdf build), copy it
# into the HTML output's _static directory so we can link to the LaTeX PDF
# from the HTML theme (CI should build latexpdf before html so the PDF
# is available).
def _copy_latex_pdf_to_static(app):
    import shutil
    import os

    # expected PDF path (relative to the repository root)
    # app.confdir is docs/source; repo root is two levels up
    repo_root = os.path.abspath(os.path.join(app.confdir, '..', '..'))
    pdf_src = os.path.join(repo_root, 'docs', 'build', 'latex', 'MusikkOgBevegelse.pdf')
    if os.path.exists(pdf_src):
        dest_static = os.path.join(app.outdir, '_static')
        os.makedirs(dest_static, exist_ok=True)
        try:
            shutil.copy2(pdf_src, os.path.join(dest_static, 'MusikkOgBevegelse.pdf'))
            app.info('[conf.py] copied LaTeX PDF into HTML _static')
        except Exception:
            # best-effort; don't raise build errors for copy failures
            pass

def setup(app):
    # run early in the build so the file is present when pages are written
    app.connect('builder-inited', _copy_latex_pdf_to_static)


# MyST options
myst_enable_extensions = [
    'colon_fence',
]

# Theme options: add an explicit download link to the LaTeX-generated PDF
html_theme_options = {
    'extra_navbar': '<a class="btn btn-primary" href="_static/MusikkOgBevegelse.pdf" target="_blank">Download PDF</a>'
}

# Include small JS that injects a LaTeX-PDF download link into the theme's download dropdown
html_js_files = [
    '_static/download_pdf.js',
]

# -- Options for LaTeX output ---------------------------------------------
latex_engine = 'xelatex'
latex_elements = {
    # The paper size ('a4paper' or 'letterpaper')
    'papersize': 'a4paper',
    # Preamble: set main font, load small typographic helpers and KOMA options.
    # Use microtype and emergencystretch to reduce overfull hboxes. Keep this
    # conservative so it works whether Sphinx emits 'book' or 'scrbook'.
    'preamble': r'''
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\usepackage{scrhack}
\usepackage{microtype}
% Allow a bit more flexibility for line breaking
\emergencystretch=1em
% Reduce aggressive hyphenation penalties
\hyphenpenalty=500
\exhyphenpenalty=500
% Set KOMA fonts for headings (harmless if not using scrbook)
\setkomafont{chapter}{\Huge\bfseries}
\setkomafont{section}{\Large\bfseries}
\setkomafont{subsection}{\large\bfseries}
\KOMAoptions{chapterprefix=true,open=right,parskip=half}
''',
}

# Further minor polish: prefer KOMA chapter handling over fncychap and set
# a simple scrlayer-scrpage header style. These are conservative tweaks that
# avoid replacing Sphinx's generated .sty files but improve heading visuals.
# (Removed: attempted scrlayer-scrpage/fncychap override — caused
# package redefinition conflicts with Sphinx-generated style files.)

# Documents to build (source start file, target name, title, author, documentclass)
latex_documents = [
    # Use scrbook (KOMA-Script) as the LaTeX document class for nicer book typography.
    # Sphinx still generates a template assuming standard 'book', but many KOMA options
    # can be set via \KOMAoptions in the preamble. If you want a full class swap,
    # consider overriding the LaTeX template in _templates/latex and changing
    # \documentclass{book} to \documentclass{scrbook} there. For now we use
    # KOMA options in the preamble to reduce template changes.
    ('index', 'MusikkOgBevegelse.tex', 'Musikk og bevegelse', 'ARJ', 'scrbook'),
]

# Add minimal KOMA options to the preamble. These are applied via \KOMAoptions
# which is safe to include even if the underlying class is 'book'—if you later
# swap to scrbook, these options will take effect. We avoid loading packages
# that conflict with sphinx defaults (e.g., titlesec) in this preamble.
latex_elements.setdefault('preamble', '')
# Set KOMA options (chapter prefix, open on right, and use parskip)
latex_elements['preamble'] += '\n\\KOMAoptions{chapterprefix=true,open=right,parskip=half}\n'
