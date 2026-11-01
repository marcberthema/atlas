PY ?= python3
TOPICS := $(shell $(PY) shared/atlas.py ids)

.PHONY: help validate build serve deploy clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'
	@echo "  make <topic>-<target>  run a topic's own target, e.g. azure-check, azure-ack SERVICE=key-vault, azure-stale"

validate:  ## Validate every topic, and check no verbatim source text is tracked
	$(PY) shared/atlas.py check
	@! git ls-files | grep -E '/(snapshots|review)/' || { echo "snapshots or review files are tracked: they must stay local"; exit 1; }
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t validate || exit 1; done

build:  ## Build every topic and the landing page into dist/
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t build || exit 1; done
	$(PY) shared/build_site.py

serve: build  ## Build and serve dist/ on http://localhost:8000
	$(PY) -m http.server 8000 --directory dist

deploy: validate build  ## Validate, build and deploy dist/ to atlas.marcberthelette.com with wrangler
	wrangler deploy

clean:  ## Remove generated output
	rm -rf dist

# make azure-check, make gitops-build, ... (add a rule here when a topic is published)
azure-%:
	$(MAKE) -C topics/azure $*
gitops-%:
	$(MAKE) -C topics/gitops $*
identity-%:
	$(MAKE) -C topics/identity $*
certificates-%:
	$(MAKE) -C topics/certificates $*
topologies-%:
	$(MAKE) -C topics/topologies $*
patterns-%:
	$(MAKE) -C topics/patterns $*
# Not a topic: kept in git, never published (outside dist/). make workstation-build, workstation-check, ...
workstation-%:
	$(MAKE) -C workstation $*
# Same for the VS Code setup: make vscode-build, vscode-check, ...
vscode-%:
	$(MAKE) -C vscode $*
