Sphinx Confluence Plugin
========================

Sphinx extension for making the documentation compatible with the Confluence Storage Format.
Read more: https://confluence.atlassian.com/display/DOC/Confluence+Storage+Format

Features:

- base HTML elements
- images (image, figure)
- code blocks (::) and includes (literalinclude)
- referencing downloadable files (:download:)
- the TOC tree (.. toctree::)
- internal links (:ref: `<label>`; .. _<label>)

Install
-------

*shell*
::

    pip install sphinx-confluence


Setup with ``conf.py``
----------------------

Plugin includes to section extensions

*python*
::

    sys.path.append('!!!_PATH_TO_EXTENSION_!!!')
    extensions = ['confluence']
    html_translator_class = 'confluence.HTMLConfluenceTranslator'
    html_add_permalinks=''


Build docs with conf.py
-----------------------


Plugin has own Builder ``json_conf``

*shell*
::

    sphinx-build -b json_conf -d build/doctrees source build/json


Build docs without conf.py
--------------------------

*shell*
::

    sphinx-build \
        -b json_conf \
        -d build/doctrees \
        -C \
        -D master_doc=index \
        -D html_add_permalinks= \
        -D html_translator_class=sphinx_confluence.HTMLConfluenceTranslator \
        -D extensions=sphinx_confluence,sphinx.ext.todo \
        source build/json
