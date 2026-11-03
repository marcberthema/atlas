#!/usr/bin/env bash
# Install the per-project part of the Claude Code setup (../README.md) into one project.
#
#   project.sh <path>                 do everything the profile's "project" section turns on, inside that project
#   project.sh <path> --only impeccable   do these items even when the profile has them off (comma separated)
#   project.sh <path> --profile my.json   another profile
#   project.sh <path> --dry-run       show what would run, and what is already done
#   project.sh --list                 list the items and whether the profile turns them on
#
# What it does: the UI skills as project-scope plugins (written to <path>/.claude/settings.json, so they follow the repository)
# and the rules block in <path>/CLAUDE.md (between markers, the rest of the file is kept). Safe to run again.
# Global things (status line, working rules, ponytail) are in setup.sh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$HERE/profile.json"; ONLY=""; DRY=0; LIST=0; PROJECT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
    *) PROJECT="$1"; shift ;;
  esac
done
source "$HERE/lib.sh"
[[ -f "$PROFILE" ]] || { echo "profile not found: $PROFILE" >&2; exit 2; }

mapfile -t ITEMS < <(profile_items project)

if [[ "$LIST" == 1 ]]; then
  for line in "${ITEMS[@]}"; do
    IFS='|' read -r kind id on _ <<<"$line"
    printf '  %-9s %-18s %s\n' "$kind" "$id" "$([[ $on == 1 ]] && echo on || echo off)"
  done
  exit 0
fi

[[ -n "$PROJECT" ]] || { echo "usage: project.sh <path to the project> [--dry-run]" >&2; exit 2; }
[[ -d "$PROJECT" ]] || { echo "not a folder: $PROJECT" >&2; exit 2; }
PROJECT="$(cd "$PROJECT" && pwd)"
have claude || { echo "claude is not installed: run the workstation setup first" >&2; exit 1; }
have python3 || { echo "python3 is required" >&2; exit 1; }
[[ "$DRY" == 1 ]] && say "dry run: nothing is changed"
say "project: $PROJECT"
[[ -d "$PROJECT/.git" ]] || warn "not a git repository: the plugin settings in .claude/ will not be tracked"

cd "$PROJECT"

step "Plugins (project scope)"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on source plugin <<<"$line"
  [[ "$kind" == plugin ]] && wanted "$id" "$on" || continue
  if [[ "$id" == taste-skill ]]; then
    node_major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
    [[ "$node_major" -ge 22 ]] || warn "taste-skill needs Node 22+ and Chrome, Edge or Chromium for its screenshot tools (found Node $node_major)"
  fi
  install_plugin "$id" "$source" "$plugin" project
done

step "Project rules"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on <<<"$line"
  [[ "$kind" == flag && "$id" == claude_md ]] && wanted claude_md "$on" && merge_block "$PROJECT/CLAUDE.md" "$HERE/project-rules.md" ui-rules
done

step "Commands"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on check cmd <<<"$line"
  [[ "$kind" == command ]] && wanted "$id" "$on" && run_item "$id" "$check" "$cmd"
done

step "Done"
say "Open Claude Code in $PROJECT and approve the project plugins when asked. Commit .claude/settings.json and CLAUDE.md if you want them to follow the repository."
true
