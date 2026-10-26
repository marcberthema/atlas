PY ?= python3

.PHONY: help validate build clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/gitops.json loads and has a title and sections
	$(PY) -c "import json; d = json.load(open('data/gitops.json')); assert d['title'] and isinstance(d['sections'], list); print('gitops ok, sections', len(d['sections']))"

build: validate  ## Generate ../../dist/gitops/index.html
	$(PY) scripts/build.py

clean:  ## Remove generated output
	rm -rf ../../dist/gitops
