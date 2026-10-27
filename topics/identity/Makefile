PY ?= python3

.PHONY: help validate build check examples clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/identity.json is consistent (exit 1 on problems)
	$(PY) scripts/validate.py

check:  ## Network: releases, archived flags, CNCF levels and code examples against the data (ONLY=id, LINKS=1 also checks source links, STRICT=1 fails on differences)
	$(PY) scripts/check_updates.py $(if $(ONLY),--only $(ONLY)) $(if $(LINKS),--links) $(if $(STRICT),--strict)
	$(PY) ../../shared/examples.py identity

examples:  ## Network: fetch the code examples from their docs pages into data/examples.json (the build reads it)
	$(PY) ../../shared/examples.py identity --refresh

build: validate  ## Generate ../../dist/identity/index.html
	$(PY) scripts/build.py

clean:  ## Remove generated output
	rm -rf ../../dist/identity
