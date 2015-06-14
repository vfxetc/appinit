SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
ALLSPHINXOPTS = $(SPHINXOPTS) .

.PHONY: html man clean

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man

clean:
	rm -rf $(BUILDDIR)/*