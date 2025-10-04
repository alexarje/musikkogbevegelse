This folder contains a minimal Sphinx + MyST project created from the `manuscript/` text files.

Quick start (recommended):

1. Create and activate a Python virtual environment (optional but recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install requirements:

   pip install -r requirements.txt

3. Build the HTML documentation:

   make -C . html

   or, if you prefer to run Sphinx directly:

   python -m sphinx -b html source build -a

4. Open the result in your browser:

   open docs/build/index.html  # or use your file manager to open the file

Notes and next steps:

- I converted the manuscript text files into `docs/source/*.md` and added a minimal `conf.py` that enables MyST. The docs build finished successfully.
- The builder produced warnings about image files not being readable. The markdown files reference images at `images/...`. If you want images to appear in the rendered site, copy the `manuscript/resources/images/` folder to `docs/source/images/` (or create a symlink):

  cp -r manuscript/resources/images docs/source/images

- If you prefer, I can copy the images for you (it may be a large number of files) or modify the markdown to point to the existing image location. Tell me which you prefer.

PDF output
----------

You can also build a PDF of the book using Sphinx's LaTeX builder. This requires a TeX toolchain (for example TeX Live) and a working LaTeX engine. Recommended engine: xelatex.

To build a PDF locally:

   make -C . latexpdf

This will create LaTeX sources and run the LaTeX engine to produce a PDF in `docs/build/latex/`.

If your machine doesn't have a TeX installation, the above command will still produce the LaTeX files under `docs/build/latex/` and you can run the following locally where TeX is available:

   ```markdown
   This folder contains the Sphinx/MyST sources and built outputs for the "Musikk og bevegelse" book.

   How to build locally

   1. Create and activate a Python virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   2. Install build dependencies (if you have a `docs/requirements.txt`):

   ```bash
   pip install -r docs/requirements.txt
   ```

   If you don't have `docs/requirements.txt`, at minimum install:

   ```bash
   pip install sphinx myst-parser
   ```

   3. Build HTML and PDF:

   ```bash
   python -m sphinx -M html docs/source docs/build
   python -m sphinx -M latexpdf docs/source docs/build
   ```

   4. The HTML output will be in `docs/build/html/` and the PDF in `docs/build/latex/`.

   Notes
   - GitHub Actions will build the HTML and attempt to build the PDF; the runner may not have a full TeX Live installation. If the PDF build fails on CI, build the PDF locally and upload it as a release artifact or host it in the repository.
   - The site is deployed from `docs/build/html` to GitHub Pages by the provided workflow.

   ```
