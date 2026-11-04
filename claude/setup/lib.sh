# Shared by setup.sh and project.sh (sourced, not run). Needs DRY, ONLY and PROFILE set by the caller.

if [[ -t 1 ]]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; N=$'\e[0m'; else B=""; G=""; Y=""; R=""; N=""; fi
say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==> %s%s\n' "$B" "$*" "$N"; }
ok()   { printf '  %sok%s   %s\n' "$G" "$N" "$*"; }
warn() { printf '%s!    %s%s\n' "$Y" "$*" "$N"; }
have() { command -v "$1" >/dev/null 2>&1; }

# run a command, or only show it with --dry-run
run() { if [[ "$DRY" == 1 ]]; then say "  would run: $*"; else "$@"; fi; }

# true when the item is on in the profile, or named in --only
wanted() { [[ ",$ONLY," == *",$1,"* ]] || [[ "$2" == 1 ]]; }

# profile_items <section>: one line per item, fields separated by "|":
#   flag|<name>|0or1   plugin|id|on|source|plugin   tool|id|on|check|install   command|id|on|check|run
profile_items() {
  python3 -I - "$PROFILE" "$1" <<'PY'
import json, sys
sec = json.load(open(sys.argv[1]))[sys.argv[2]]
for k, v in sec.items():
    if isinstance(v, bool):
        print(f"flag|{k}|{int(v)}")
for p in sec.get("plugins", []):
    print(f"plugin|{p['id']}|{int(p['on'])}|{p['source']}|{p['plugin']}")
for t in sec.get("tools", []):
    print(f"tool|{t['id']}|{int(t['on'])}|{t['check']}|{t['install']}")
for c in sec.get("commands", []):
    print(f"command|{c['id']}|{int(c['on'])}|{c['check']}|{c['run']}")
PY
}

# plugin_present <plugin@marketplace> <scope>: installed and enabled at that scope. A project-scope plugin counts only for the current
# folder (`claude plugin list` shows the plugins of every project, as disabled ones in the others).
plugin_present() {
  claude plugin list --json 2>/dev/null | python3 -I -c '
import json, os, sys
plug, scope, here = sys.argv[1], sys.argv[2], os.path.realpath(os.getcwd())
for p in json.load(sys.stdin):
    if p["id"] == plug and p["scope"] == scope and p.get("enabled") and (scope != "project" or os.path.realpath(p.get("projectPath", "")) == here):
        sys.exit(0)
sys.exit(1)' "$1" "$2"
}

# install_plugin <id> <source> <plugin@marketplace> <scope>: skipped when already installed at that scope (project scope: run from the project)
install_plugin() {
  local id="$1" src="$2" plug="$3" scope="$4"
  if plugin_present "$plug" "$scope"; then ok "$id (already installed)"; return; fi
  say "  add  $id: $plug ($scope)"
  run claude plugin marketplace add --scope "$scope" "$src"
  run claude plugin install --scope "$scope" "$plug"
}

# run_item <id> <check> <command>: run the command unless the check already succeeds
run_item() {
  if bash -c "$2" >/dev/null 2>&1; then ok "$1 (already done)"; return; fi
  say "  run  $1: $3"
  run bash -c "$3"
}

# merge_block <file> <block file> <name>: put the block between markers in the file, replacing an earlier copy.
# The file is created when missing; an existing file is backed up once, the first time a block is added.
merge_block() {
  local file="$1" block="$2" name="$3"
  python3 -I - "$file" "$block" "$name" "$DRY" <<'PY'
import shutil, subprocess, sys, time
from pathlib import Path
file, block, name, dry = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4] == "1"
begin, end = f"<!-- atlas claude setup: {name} begin -->", f"<!-- atlas claude setup: {name} end -->"
new = f"{begin}\n{block.read_text().strip()}\n{end}\n"
old = file.read_text() if file.exists() else ""
if begin in old and end in old:
    head, rest = old.split(begin, 1)
    tail = rest.split(end, 1)[1].lstrip("\n")
    out = head + new + (("\n" + tail) if tail else "")
else:
    out = (old.rstrip("\n") + "\n\n" if old.strip() else "") + new
if out == old:
    print(f"  ok   {file} ({name} block already current)")
elif dry:
    print(f"  would write the {name} block into {file}")
else:
    tracked = old and subprocess.run(["git", "-C", str(file.parent), "ls-files", "--error-unmatch", file.name],
                                     capture_output=True).returncode == 0   # git is the backup of a tracked file
    if old and begin not in old and not tracked:
        shutil.copy(file, f"{file}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        print(f"  previous {file} backed up next to it")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(out)
    print(f"  wrote the {name} block into {file}")
PY
}
