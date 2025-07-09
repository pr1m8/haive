# docs/Makefile
SPHINXOPTS    ?= -W --keep-going
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help Makefile

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)
	rm -rf $(SOURCEDIR)/api/generated

html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

livehtml:
	poetry run sphinx-autobuild "$(SOURCEDIR)" "_build/html" \
		--port 8003 \
		--host 0.0.0.0 \
		--ignore "*.pyc" \
		--ignore "*.pyo" \
		--ignore ".git/*" \
		--ignore "_build/*" \
		--watch ../packages \
		--open-browser \
		-j auto

# Catch-all target
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)