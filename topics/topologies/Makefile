PY ?= python3

.PHONY: help validate build check clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/topologies.json is consistent (exit 1 on problems)
	$(PY) scripts/validate.py

check:  ## Network: releases, archived flags and CNCF levels against the data (ONLY=id, LINKS=1 also checks source links, STRICT=1 fails on differences)
	$(PY) scripts/check_updates.py $(if $(ONLY),--only $(ONLY)) $(if $(LINKS),--links) $(if $(STRICT),--strict)

build: validate  ## Generate ../../dist/topologies/index.html
	$(PY) scripts/build.py

clean:  ## Remove generated output
	rm -rf ../../dist/topologies
