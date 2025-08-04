# Overall

# Documentation

## Formatting Issues

- CSS FIle revamp
- Usage of script to check the pictures
- Api vs non api
- Overall Styliung, theme colours
- Broken imporst

# Package Wise

## Root

- [] Migrate to 3.13
- [] Use uv

## Haive-Core

### Document Loading

- [] (haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group document_loaders pybtex pypdfium2 pdfminer youtube-transcript-api docx selenium pdfplumber pytesseract ebooklib google-cloud-storage notion-client google-auth beautifulsoup4 vsdx extract-msg web3 shareplum pyairtable cassandra-driver couchbase airbyte-cdk duckdb mwxml conllu atlassian-python-api pyyaml
- [] Fix the other loader issues form langchain_community
- [] Perssistence Issues
  -poetry add --group docs sphinx breathe docxsphinx javasphinx numpydoc sphinx-gallery sphinx-git sphinx-jekyll-builder sphinx-markdown-builder sphinx-prompt sphinx-pyreverse sphinxcontrib-autoprogram sphinxcontrib-blockdiag sphinxcontrib-constdata sphinxcontrib-cldomain sphinxcontrib-docbookrestapi sphinxcontrib-fulltoc sphinxcontrib-httpdomain sphinxcontrib-programoutput sphinxcontrib-napoleon tut sphinx-needs nbsphinx sphinxcontrib-proof sphinxcontrib-packages sphinx-sitemap sphinx-jsonschema sphinx-gitstamp sphinx-intl django-sphinxdoc sphobjinv myst-parser jupyter-book alabaster flask-sphinx-themes sphinx-readable-theme sphinx-better-theme sphinx-rtd-theme sphinx-typo3-theme sphinx-py3doc-enhanced-theme sphinx-bootstrap-theme sphinx-foundation-theme sphinx-nameko-theme crate-docs-theme solar-theme mdn-sphinx-theme sphinx-adc-theme sphinx-autobuild ghp-import okydoky
  ll@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ source .venv/bin/activate
  (haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev typer rich libcst pydantic gitpython
  Using version ^0.16.0 for typer
  Using version ^14.0.0 for rich
  Using version ^1.8.2 for libcst
  Using version ^2.11.7 for pydantic
  Using version ^3.1.44 for gitpython

Updating dependencies
Resolving dependencies... (0.0s)

Incompatible constraints in requirements of haive (0.1.0):
rich (>=13.9.4,<14.0.0)
rich (>=14.0.0,<15.0.0)
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev black isort autoflake add-trailing-comma absolufy-imports autopep8 yapf reindent
The following packages are already present in the pyproject.toml and will be skipped:

- black
- isort
- autoflake
- add-trailing-comma
- absolufy-imports
- autopep8
- yapf
- reindent

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev interrogate pydocstyle darglint pydocstringformatter
The following packages are already present in the pyproject.toml and will be skipped:

- interrogate
- pydocstyle
- darglint
- pydocstringformatter

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev syntax-checker tomli-w tomli factory-boy mimesis
The following packages are already present in the pyproject.toml and will be skipped:

- syntax-checker
- tomli-w
- tomli
- factory-boy
- mimesis

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev pre-commit towncrier nbstripout pipdeptree rstcheck
The following packages are already present in the pyproject.toml and will be skipped:

- pre-commit
- towncrier
- nbstripout
- pipdeptree
- rstcheck

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev viztracer memray py-spy
The following packages are already present in the pyproject.toml and will be skipped:

- viztracer
- memray
- py-spy

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev pytest pytest-asyncio pytest-rich pytest-clarity pytest-html pytest-sugar hypothesis coverage tox
The following packages are already present in the pyproject.toml and will be skipped:

- pytest
- pytest-asyncio
- pytest-rich
- pytest-clarity
- pytest-html
- pytest-sugar
- hypothesis
- coverage
- tox

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev interrogate pydocstyle darglint pydocstringformatter
The following packages are already present in the pyproject.toml and will be skipped:

- interrogate
- pydocstyle
- darglint
- pydocstringformatter

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev pycycle
Using version ^0.0.8 for pycycle

Updating dependencies
Resolving dependencies... (3.2s)

module 'posixpath' has no attribute 'ALLOW_MISSING'
(haive-py3.12) will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ poetry add --group dev abs2rel
Using version ^1.1.0 for abs2rel

Updating dependencies
Resolving dependencies... (1.2s)

## Haive-Agents

- [] React Agent: Tool and engine sync, executor mixin
- [] Simple Agent: Lack of using token tracking
- [] Reflection/Reflexion
- [] S/o - hooks mixin
