PY ?= python3
TOPICS := azure gitops

.PHONY: help validate build serve clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'
	@echo "  make <topic>-<target>  run a topic's own target, e.g. azure-check, azure-ack SERVICE=key-vault, azure-stale"

validate:  ## Validate every topic, and check no verbatim source text is tracked
	@! git ls-files | grep -E '/(snapshots|review)/' || { echo "snapshots or review files are tracked: they must stay local"; exit 1; }
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t validate || exit 1; done

build:  ## Build every topic and the landing page into dist/
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t build || exit 1; done
	$(PY) shared/build_site.py

serve: build  ## Build and serve dist/ on http://localhost:8000
	$(PY) -m http.server 8000 --directory dist

clean:  ## Remove generated output
	rm -rf dist

# make azure-check, make gitops-build, ...
azure-%:
	$(MAKE) -C topics/azure $*
gitops-%:
	$(MAKE) -C topics/gitops $*
