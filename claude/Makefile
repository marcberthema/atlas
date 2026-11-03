.PHONY: help list setup-dry-run setup project-list project-dry-run project

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-16s %s\n", $$1, $$2}'

list:  ## List the global items and whether the profile turns them on
	setup/setup.sh --list

setup-dry-run:  ## Show what the global setup would install and change (changes nothing)
	setup/setup.sh --dry-run

setup:  ## Install the global setup for this account: status line, working rules, plugins (ARGS="--only superpowers")
	setup/setup.sh $(ARGS)

project-list:  ## List the per-project items and whether the profile turns them on
	setup/project.sh --list

project-dry-run:  ## Show what would be installed in PROJECT=<path> (changes nothing)
	setup/project.sh "$(PROJECT)" --dry-run

project:  ## Install the per-project plugins and rules into PROJECT=<path> (ARGS="--only playwright-skills")
	setup/project.sh "$(PROJECT)" $(ARGS)
