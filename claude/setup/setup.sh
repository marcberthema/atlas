#!/usr/bin/env bash
# Install the Claude Code setup (../README.md) at the global level, for the account that runs it.
#
#   setup.sh                    do everything the profile's "global" section turns on
#   setup.sh --only ponytail    do these items even when the profile has them off (comma separated)
#   setup.sh --profile my.json  another profile (copy profile.json and edit it)
#   setup.sh --dry-run          show what would run, and what is already done
#   setup.sh --list             list the items and whether the profile turns them on
#
# What it does: the status line (the script is shared with workstation/), the working rules in ~/.claude/CLAUDE.md (between markers,
# the rest of the file is kept), the plugins and the tools. Safe to run again: what is done is skipped. Needs claude and python3.
# Per project things (UI skills, project rules) are in project.sh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$HERE/profile.json"; ONLY=""; DRY=0; LIST=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done
source "$HERE/lib.sh"
[[ -f "$PROFILE" ]] || { echo "profile not found: $PROFILE" >&2; exit 2; }

STATUSLINE_SRC="$HERE/../../workstation/setup/claude-statusline.py"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"   # for tests: point it at a throwaway folder

do_statusline() {
  if cmp -s "$STATUSLINE_SRC" "$CLAUDE_HOME/statusline.py" && grep -q statusline.py "$CLAUDE_HOME/settings.json" 2>/dev/null; then
    ok "status line (already installed)"; return
  fi
  say "  add  status line: model, effort, folder, branch, context, 5h and 7d usage"
  [[ "$DRY" == 1 ]] && return
  mkdir -p "$CLAUDE_HOME"
  install -m 0755 "$STATUSLINE_SRC" "$CLAUDE_HOME/statusline.py"
  # Set statusLine and keep every other setting
  python3 -I - "$CLAUDE_HOME/settings.json" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
s = json.loads(p.read_text()) if p.exists() else {}
s["statusLine"] = {"type": "command", "command": "~/.claude/statusline.py", "refreshInterval": 60}
p.write_text(json.dumps(s, indent=2) + "\n")
PY
}

mapfile -t ITEMS < <(profile_items global)

if [[ "$LIST" == 1 ]]; then
  for line in "${ITEMS[@]}"; do
    IFS='|' read -r kind id on _ <<<"$line"
    [[ "$kind" == flag ]] && { id="$id"; }
    printf '  %-9s %-18s %s\n' "$kind" "$id" "$([[ $on == 1 ]] && echo on || echo off)"
  done
  exit 0
fi

have claude || { echo "claude is not installed: run the workstation setup first (or https://claude.ai/install.sh)" >&2; exit 1; }
have python3 || { echo "python3 is required" >&2; exit 1; }
[[ "$DRY" == 1 ]] && say "dry run: nothing is changed"

step "Status line and working rules"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on <<<"$line"
  [[ "$kind" == flag ]] || continue
  case "$id" in
    statusline) if wanted statusline "$on"; then do_statusline; fi ;;
    rules) if wanted rules "$on"; then merge_block "$CLAUDE_HOME/CLAUDE.md" "$HERE/global-rules.md" rules; fi ;;
  esac
done

step "Plugins (user scope)"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on source plugin <<<"$line"
  [[ "$kind" == plugin ]] && wanted "$id" "$on" && install_plugin "$id" "$source" "$plugin" user
done

step "Tools"
for line in "${ITEMS[@]}"; do
  IFS='|' read -r kind id on check install <<<"$line"
  [[ "$kind" == tool ]] && wanted "$id" "$on" && run_item "$id" "$check" "$install"
done

step "Done"
say "Start a new Claude Code session to load the status line and plugins. Per project: make project PROJECT=<path>"
true
