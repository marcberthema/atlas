PY ?= python3

.PHONY: help validate build check examples clean setup setup-dry-run win-setup win-dry-run win-list

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-14s %s\n", $$1, $$2}'

validate:  ## Check data/workstation.json is consistent (exit 1 on problems)
	$(PY) scripts/validate.py

check:  ## Network: releases, archived flags, CNCF levels and code examples against the data (ONLY=id, LINKS=1 also checks source links, STRICT=1 fails on differences)
	$(PY) scripts/check_updates.py $(if $(ONLY),--only $(ONLY)) $(if $(LINKS),--links) $(if $(STRICT),--strict)
	$(PY) ../shared/examples.py workstation --dir .

examples:  ## Network: fetch the code examples from their docs pages into data/examples.json (the build reads it)
	$(PY) ../shared/examples.py workstation --dir . --refresh

build: validate  ## Generate site/index.html (not published: outside dist/)
	$(PY) scripts/build.py

setup-dry-run:  ## WSL: show what setup.sh would run (changes nothing)
	setup/setup.sh --dry-run

setup:  ## WSL: install and configure from setup/profile.json, then clone its repos into ~/git (ARGS="--only helm")
	setup/setup.sh $(ARGS)

win-list:  ## Git Bash on Windows: list the Windows profile (changes nothing)
	setup/setup-windows.sh --list

win-dry-run:  ## Git Bash on Windows: show what would be installed and cloned (changes nothing)
	setup/setup-windows.sh --dry-run

win-setup:  ## Git Bash on Windows, no admin: Scoop tools under C:/work/tools, repos into C:/work/git (ARGS="--only jq")
	setup/setup-windows.sh $(ARGS)

clean:  ## Remove generated output
	rm -rf site
