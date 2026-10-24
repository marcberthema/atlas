PY ?= python3

.PHONY: help validate build check check-service ack stale update serve clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/services.json is consistent (exit 1 on problems)
	$(PY) scripts/validate.py

build: validate  ## Generate dist/index.html and dist/services.resolved.json
	$(PY) scripts/build.py

check:  ## Daily freshness check: Learn pages and Terraform support (writes data/services.json)
	$(PY) scripts/check_updates.py check

check-service:  ## Same for one service: make check-service SERVICE=key-vault
	$(PY) scripts/check_updates.py check --only $(SERVICE)

ack:  ## Mark current Learn content as reviewed: make ack SERVICE=key-vault (or all)
	$(PY) scripts/check_updates.py ack $(SERVICE)

stale:  ## List what needs review and write review/PROMPT.md for an AI agent (ALL=1 adds never-reviewed, LIMIT=n caps it)
	$(PY) scripts/stale.py $(if $(ALL),--all) $(if $(LIMIT),--limit $(LIMIT))

update: check build  ## check, then rebuild the page

serve: build  ## Build and serve dist/ on http://localhost:8000
	$(PY) -m http.server 8000 --directory dist

clean:  ## Remove generated output
	rm -rf dist
