# Data model

`data/terraform.json` follows the same format as the GitOps topic: see `topics/gitops/docs/data-model.md` for entries, learning layout,
code examples and the update check.

Terraform specifics:

- Groups: `core` (the tab entries, about the CLI and language), `tools` (companion tools) and `alternative` (OpenTofu).
- `license` is `BUSL-1.1` for the Terraform entries. `cncf.level` is `none` unless cncf.io says otherwise.
- `track.tag` is a regex for release tags (`^v\d+\.\d+\.\d+$`), so the check ignores prereleases and non-version tags.
