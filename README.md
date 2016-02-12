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
- Inline and table Jira Issues
- Reference for Confluence User
- Info, Tip, Note, and Warning Macros

Jira Issues
-----------

**Inline**

```rst
Lorem ipsum dolor sit amet, :jira_issue:`PROJECT-123` consectetur adipiscing elit
```

**Table View**


*Markup:*

```rst
.. jira_issues:: <JQL query>
   :anonymous: 'true'|'false' (default: 'false')
   :server_id: 'string' (default: '')
   :baseurl: 'string' (default: '')
   :columns: A list of JIRA column names, separated by semi-colons (;)
   :count: 'true'|'false' (default: 'false')
   :height: int (default: 480)
   :title: 'string' (default: '')
   :render_mode: 'static'|'dynamic' (default: 'static')
   :url: 'string' (default: '')
   :width: '{x}px' | '{x}%' (default: '100%')
   :maximum_issues: int (default: 20)
```

*Example:*

```rst
.. jira_issues:: project = PROJ AND issuetype = Epic AND resolution = Unresolved
   :title: Unresolved project epics
   :columns: type;key;summary;status;created;
   :width: 80%
```

Jira Users
----------

```rst
Lorem ipsum dolor sit amet, :jira_user:`username` consectetur adipiscing elit
```


Install
-------
```pip install sphinx-confluence```


Setup with ``conf.py``
----------------------

Plugin includes to section extensions

```python
import sys
sys.path.append('!!!_PATH_TO_EXTENSION_!!!')
extensions = ['sphinx_confluence']
```

Build docs with conf.py
-----------------------


Plugin has own Builder ``json_conf`` (deprecated: use ``json`` instead)

```sh
sphinx-build -b json -d build/doctrees source build/json
```

Build docs without conf.py
--------------------------

```sh
    sphinx-build \
        -b json \
        -d build/doctrees \
        -C \
        -D master_doc=index \
        -D extensions=sphinx_confluence,sphinx.ext.todo \
        source build/result
```
