PY ?= python3
TOPICS := $(shell $(PY) shared/atlas.py ids)

.PHONY: help validate build serve deploy clean lenses-check

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'
	@echo "  make <topic>-<target>  run a topic's own target, e.g. azure-check, azure-ack SERVICE=key-vault, azure-stale"

validate:  ## Validate every topic, and check no verbatim source text is tracked
	$(PY) shared/atlas.py check
	$(PY) shared/spec.py
	$(PY) shared/lenses_check.py
	@! git ls-files | grep -E '/(snapshots|review)/' || { echo "snapshots or review files are tracked: they must stay local"; exit 1; }
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t validate || exit 1; done

build:  ## Build every topic and the landing page into dist/
	@for t in $(TOPICS); do $(MAKE) --no-print-directory -C topics/$$t build || exit 1; done
	$(PY) shared/build_views.py
	$(PY) shared/build_lenses.py
	$(PY) shared/build_site.py

serve: build  ## Build and serve dist/ on http://localhost:8000
	$(PY) -m http.server 8000 --directory dist

deploy: validate  ## Validate, build (stamping the git ref shown in the About window) and deploy dist/ to atlas.marcberthelette.com with wrangler
	ATLAS_REF=$$(git describe --tags --always --dirty) $(MAKE) build
	wrangler deploy

clean:  ## Remove generated output
	rm -rf dist

# make azure-check, make gitops-build, ... (add a rule here when a topic is published)
azure-%:
	$(MAKE) -C topics/azure $*
gitops-%:
	$(MAKE) -C topics/gitops $*
terraform-%:
	$(MAKE) -C topics/terraform $*
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
github-actions-%:
	$(MAKE) -C topics/github-actions $*
# The lenses view (views/lenses/): make lenses-check also fetches every source url
lenses-check:  ## Check the lenses data and that its source links still answer (network)
	$(PY) shared/lenses_check.py links
# Same for the Claude Code setup: make claude-setup, claude-project PROJECT=<path>, ...
claude-%:
	$(MAKE) -C claude $*
cloudflare-%:
	$(MAKE) -C topics/cloudflare $*
workos-%:
	$(MAKE) -C topics/workos $*
