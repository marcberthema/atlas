PY ?= python3

.PHONY: help validate build clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/gitops.json is consistent (exit 1 on problems)
	$(PY) scripts/validate.py

build: validate  ## Generate ../../dist/gitops/index.html
	$(PY) scripts/build.py

clean:  ## Remove generated output
	rm -rf ../../dist/gitops
