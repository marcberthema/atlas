#!/usr/bin/env bash
# Install and configure Visual Studio Code for WSL Ubuntu (../site/index.html) from a JSON profile.
#
#   setup.sh                        install the extensions the profile turns on, then merge the settings groups it turns on
#   setup.sh --profile my.json      another profile (copy profile.json and edit it)
#   setup.sh --only ruff,terraform  only these: extension ids or settings group names, even when the profile has them off
#   setup.sh --dry-run              show what is installed, what would be installed and which settings would change
#   setup.sh --list                 list the profile
#   setup.sh --no-extensions        settings only         --no-settings   extensions only
#   setup.sh --settings-file PATH   merge into this file instead of the Windows user settings.json
#
# Run it in Ubuntu (WSL) as your normal user, after installing VS Code on Windows with "Add to PATH" checked. No sudo needed.
# Safe to run again: an installed extension is skipped, a setting already at its value is left alone. Needs python3 (Ubuntu has it).
# An extension id may be given in --only without its publisher when it is unique: ruff, terraform, claude-code.
# VS Code is found through `code` on the PATH or its usual Windows folders; set VSCODE_CODE=/path/to/bin/code for another place.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$HERE/profile.json"
ONLY=""; DRY=0; LIST=0; DO_EXT=1; DO_SET=1; SETTINGS_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    --no-extensions) DO_EXT=0; shift ;;
    --no-settings) DO_SET=0; shift ;;
    --settings-file) SETTINGS_FILE="$2"; shift 2 ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

if [[ -t 1 ]]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; N=$'\e[0m'; else B=""; G=""; Y=""; R=""; N=""; fi
say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==> %s%s\n' "$B" "$*" "$N"; }
warn() { printf '%s!   %s%s\n' "$Y" "$*" "$N"; }

[[ -f "$PROFILE" ]] || { echo "profile not found: $PROFILE" >&2; exit 2; }

# --- Profile: one line per extension "id|on|where", read once ----------------------------------------------------------
mapfile -t EXT_LINES < <(python3 -I - "$PROFILE" <<'PY'
import json, sys
for k, v in json.load(open(sys.argv[1]))["extensions"].items():
    print(f'{k}|{1 if v["on"] else 0}|{v["where"]}')
PY
)
declare -A EXT_ON EXT_WHERE
EXT_IDS=()
for line in "${EXT_LINES[@]}"; do
  IFS='|' read -r id on where <<<"$line"
  EXT_IDS+=("$id"); EXT_ON["$id"]="$on"; EXT_WHERE["$id"]="$where"
done

# --only names: a full id, a settings group, or the part after the publisher's dot (ruff -> charliermarsh.ruff)
resolve_only() {
  local name="${1,,}" id lc found=()
  for id in "${EXT_IDS[@]}"; do
    lc="${id,,}"
    # the full id, or a whole hyphen-separated word of the part after the publisher: ruff, terraform, claude-code, wsl, yaml
    if [[ "$lc" == "$name" || "-${lc#*.}-" == *"-$name-"* ]]; then found+=("$id"); fi
  done
  if [[ ${#found[@]} -eq 1 ]]; then echo "${found[0]}"; return 0; fi
  if [[ ${#found[@]} -gt 1 ]]; then echo "ambiguous --only name '$1': ${found[*]}" >&2; exit 2; fi
  echo "$1"
}
FORCED_EXT=(); FORCED_GROUPS=()
GROUPS_IN_PROFILE="$(python3 -I - "$PROFILE" <<'PY'
import json, sys
print(" ".join(json.load(open(sys.argv[1])).get("settings", {})))
PY
)"
if [[ -n "$ONLY" ]]; then
  for n in ${ONLY//,/ }; do
    if [[ " $GROUPS_IN_PROFILE " == *" $n "* ]]; then FORCED_GROUPS+=("$n"); continue; fi
    r="$(resolve_only "$n")"
    if [[ -n "${EXT_WHERE[$r]:-}" ]]; then FORCED_EXT+=("$r"); else echo "unknown extension or settings group in --only: $n" >&2; exit 2; fi
  done
fi
forced() { local x; for x in "${FORCED_EXT[@]}"; do [[ "$x" == "$1" ]] && return 0; done; return 1; }
selected_ext() {
  if [[ -n "$ONLY" ]]; then forced "$1"; else [[ "${EXT_ON[$1]}" == 1 ]]; fi
}

# --- --list ---------------------------------------------------------------------------------------------------------------
if [[ $LIST == 1 ]]; then
  say "${B}profile:${N} $PROFILE"
  for id in "${EXT_IDS[@]}"; do
    if [[ "${EXT_ON[$id]}" == 1 ]]; then printf '  %s on %s  %-46s %s\n' "$G" "$N" "$id" "${EXT_WHERE[$id]}"; else printf '  %s off%s  %-46s %s\n' "$Y" "$N" "$id" "${EXT_WHERE[$id]}"; fi
  done
  python3 -I - "$PROFILE" <<'PY'
import json, sys
for k, g in json.load(open(sys.argv[1])).get("settings", {}).items():
    print(f'  settings  {k:<16} {"on " if g["on"] else "off"}  {len(g["values"])} key(s)' + (f'  needs {", ".join(g["needs"])}' if g.get("needs") else ""))
PY
  exit 0
fi

# --- Find VS Code from WSL ------------------------------------------------------------------------------------------------
# VS Code is installed on Windows. Its bin/code script, run from WSL, checks for the WSL extension (ms-vscode-remote.remote-wsl):
# with it, commands go to the WSL side (the extension's own script, extensions in ~/.vscode-server); without it, to the Windows CLI.
# So the WSL extension is installed first, through the Windows CLI that the launcher script itself uses, then the rest through `code`.
win_env() { (cd /mnt/c && cmd.exe /c "echo %$1%" 2>/dev/null | tr -d '\r'); }
find_code() {
  local c cand
  [[ -n "${VSCODE_CODE:-}" ]] && { echo "$VSCODE_CODE"; return 0; }   # a VS Code in an unusual place: VSCODE_CODE=/path/to/bin/code
  if c="$(command -v code 2>/dev/null)" && [[ "$c" == /mnt/* ]]; then echo "$c"; return 0; fi
  for cand in "$(wslpath -u "$(win_env LOCALAPPDATA)" 2>/dev/null)/Programs/Microsoft VS Code/bin/code" "/mnt/c/Program Files/Microsoft VS Code/bin/code"; do
    [[ -f "$cand" ]] && { echo "$cand"; return 0; }
  done
  return 1
}
CODE=""; VSCODE_PATH=""; ELECTRON=""; CLI=""
if CODE="$(find_code)"; then
  VSCODE_PATH="$(dirname "$(dirname "$(realpath "$CODE")")")"
  ELECTRON="$VSCODE_PATH/Code.exe"
  verfolder="$(sed -n 's/^VERSIONFOLDER="\(.*\)"/\1/p' "$CODE")"
  CLI="$VSCODE_PATH/$verfolder/resources/app/out/cli.js"
fi
win_code() { WSLENV="ELECTRON_RUN_AS_NODE/w:${WSLENV:-}" ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$(wslpath -m "$CLI")" "$@"; }

SERVER_EXT_DIR="$HOME/.vscode-server/extensions"
wsl_installed() {   # ids of extensions inside WSL, lowercase: folders are publisher.name-version[-platform]
  [[ -d "$SERVER_EXT_DIR" ]] || return 0
  ls -1 "$SERVER_EXT_DIR" 2>/dev/null | grep -v '^extensions.json$' | sed -E 's/-[0-9].*//' | tr 'A-Z' 'a-z' | sort -u
}
win_installed() { [[ -n "$CODE" ]] && win_code --list-extensions 2>/dev/null | tr -d '\r' | tr 'A-Z' 'a-z' | sort -u || true; }

# --- Extensions -----------------------------------------------------------------------------------------------------------
DONE=(); SKIPPED=(); FAILED=()
install_extensions() {
  step "extensions"
  if [[ -z "$CODE" ]]; then
    warn "VS Code was not found. Install it on Windows (winget.exe install Microsoft.VisualStudioCode from WSL, or code.visualstudio.com) and check 'Add to PATH'."
    return 1
  fi
  say "VS Code: $VSCODE_PATH  ($(win_code --version 2>/dev/null | head -1 | tr -d '\r'))"
  local have_win have_wsl id where
  have_win="$(win_installed)"; have_wsl="$(wsl_installed)"
  # the Windows-side ones first: the WSL extension decides where the later commands go
  for pass in windows wsl; do
    for id in "${EXT_IDS[@]}"; do
      [[ "${EXT_WHERE[$id]}" == "$pass" ]] && selected_ext "$id" || continue
      local lc="${id,,}" present=0
      if [[ $pass == windows ]]; then grep -qx "$lc" <<<"$have_win" && present=1; else grep -qx "$lc" <<<"$have_wsl" && present=1; fi
      if [[ $present == 1 && -z "$ONLY" ]]; then say "  = $id ($pass) already installed"; SKIPPED+=("$id"); continue; fi
      if [[ $DRY == 1 ]]; then say "  + $id ($pass) would be $([[ $present == 1 ]] && echo updated || echo installed)"; continue; fi
      local now_win; now_win="$(win_installed)"
      if [[ $pass == wsl ]] && ! grep -qx "ms-vscode-remote.remote-wsl" <<<"$now_win"; then
        warn "$id: the WSL extension is not installed, so 'code' would install it on Windows. Turn on ms-vscode-remote.remote-wsl first."
        FAILED+=("$id"); continue
      fi
      say "  + $id ($pass)"
      local out rc=0
      if [[ $pass == windows ]]; then out="$(win_code --install-extension "$id" --force 2>&1)" || rc=$?; else out="$("$CODE" --install-extension "$id" --force 2>&1)" || rc=$?; fi
      if [[ $rc -ne 0 ]] || grep -qi "failed installing\|not found\|incompatible\|error" <<<"$out"; then
        printf '%s' "$out" | tail -3 | sed 's/^/      /'
        FAILED+=("$id"); continue
      fi
      # check it landed where it should
      local now_wsl; now_wsl="$(wsl_installed)"
      if [[ $pass == wsl ]] && ! grep -qx "$lc" <<<"$now_wsl"; then
        warn "$id: the command succeeded but $SERVER_EXT_DIR has no folder for it. Open a folder with 'code .' once, then run this again."
        FAILED+=("$id"); continue
      fi
      DONE+=("$id")
    done
  done
  return 0
}

# --- Settings -------------------------------------------------------------------------------------------------------------
merge_settings() {
  step "settings"
  local target="$SETTINGS_FILE"
  if [[ -z "$target" ]]; then
    local appdata; appdata="$(win_env APPDATA)"
    [[ -n "$appdata" ]] || { warn "could not find the Windows %APPDATA%. Pass --settings-file PATH."; return 1; }
    target="$(wslpath -u "$appdata")/Code/User/settings.json"
  fi
  # extensions that count as present for a group's "needs": on in the profile, installed, or named in --only
  local present="" id
  for id in "${EXT_IDS[@]}"; do { [[ "${EXT_ON[$id]}" == 1 ]] || forced "$id"; } && present+="${id,,} "; done
  present+="$(wsl_installed | tr '\n' ' ') $(win_installed | tr '\n' ' ')"
  python3 -I - "$PROFILE" "$target" "$DRY" "$present" "${FORCED_GROUPS[*]:-}" "${ONLY:+1}" <<'PY'
import datetime, json, os, shutil, sys
profile, target, dry, present, forced, only = sys.argv[1], sys.argv[2], sys.argv[3] == "1", set(sys.argv[4].lower().split()), set(sys.argv[5].split()), bool(sys.argv[6])


def strip_jsonc(text):
    """settings.json is JSON with comments and trailing commas. Returns (plain json text, whether comments were found)."""
    out, i, n, found, in_str = [], 0, len(text), False, False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1]); i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True; out.append(c)
        elif text.startswith("//", i):
            found = True
            while i < n and text[i] != "\n": i += 1
            continue
        elif text.startswith("/*", i):
            found = True
            end = text.find("*/", i)
            if end < 0:
                raise ValueError("a /* comment is never closed")
            i = end + 2
            continue
        else:
            out.append(c)
        i += 1
    plain = "".join(out)
    # trailing commas: a comma followed only by whitespace and a closing bracket
    res, in_str, i = [], False, 0
    while i < len(plain):
        c = plain[i]
        if in_str:
            res.append(c)
            if c == "\\" and i + 1 < len(plain): res.append(plain[i + 1]); i += 1
            elif c == '"': in_str = False
        elif c == '"':
            in_str = True; res.append(c)
        elif c == ",":
            j = i + 1
            while j < len(plain) and plain[j] in " \t\r\n": j += 1
            if not (j < len(plain) and plain[j] in "}]"):   # a trailing comma is dropped
                res.append(c)
        else:
            res.append(c)
        i += 1
    return "".join(res), found


def merge(dst, src, path, changes):
    for k, v in src.items():
        here = f"{path}{k}"
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            merge(dst[k], v, here + " > ", changes)
        elif dst.get(k) != v:
            changes.append((here, dst.get(k, "(not set)"), v))
            dst[k] = v


groups = json.load(open(profile)).get("settings", {})
wanted, skipped = {}, []
for name, g in groups.items():
    if (only and name not in forced) or (not only and not g["on"]):
        continue
    missing = [x for x in g.get("needs", []) if x.lower() not in present]
    if missing:
        skipped.append(f'{name} (needs {", ".join(missing)})'); continue
    wanted[name] = g["values"]
if not wanted:
    print("  no settings groups selected" + (f"; skipped: {', '.join(skipped)}" if skipped else "")); sys.exit(0)

exists = os.path.exists(target) and os.path.getsize(target) > 0
current, has_comments = {}, False
if exists:
    try:
        plain, has_comments = strip_jsonc(open(target, encoding="utf-8").read())
        current = json.loads(plain)
    except ValueError as e:
        print(f"  {target} is not valid JSON ({e}). Fix it first; nothing was written."); sys.exit(4)
    if not isinstance(current, dict):
        print(f"  {target} is not a JSON object; nothing was written."); sys.exit(4)

merged, changes = json.loads(json.dumps(current)), []
for name, values in wanted.items():
    merge(merged, values, "", changes)
print(f"  file: {target}" + ("" if exists else " (does not exist yet)"))
print(f"  groups: {', '.join(wanted)}" + (f"   skipped: {', '.join(skipped)}" if skipped else ""))
if not changes:
    print("  already up to date"); sys.exit(0)
for key, old, new in changes:
    print(f"  {'set' if old == '(not set)' else 'change'}  {key}: " + (f"{json.dumps(old)} -> " if old != "(not set)" else "") + json.dumps(new))
if has_comments:
    print("  The file has comments, and rewriting it would drop them. Nothing was written.")
    print("  Merge these groups into it by hand (the values are in the profile), or remove the comments and run this again."); sys.exit(3)
if dry:
    print("  (dry run: nothing written)"); sys.exit(0)
os.makedirs(os.path.dirname(target), exist_ok=True)
if exists:
    bak = f"{target}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(target, bak)
    print(f"  backup: {bak}")
tmp = target + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(merged, f, indent=4, ensure_ascii=False); f.write("\n")
os.replace(tmp, target)
print("  written")
PY
}

# --- Run ------------------------------------------------------------------------------------------------------------------
[[ $EUID -ne 0 ]] || { echo "run as your normal user, not root" >&2; exit 1; }
grep -qi microsoft /proc/version || warn "not running in WSL: the VS Code lookup and the Windows settings path will not work"
say "${B}profile:${N} $PROFILE"
[[ $DRY == 1 ]] && say "(dry run: nothing is installed or written)"

rc=0
if [[ $DO_EXT == 1 ]]; then install_extensions || rc=1; fi
if [[ $DO_SET == 1 ]]; then merge_settings || rc=1; fi

step "summary"
say "${G}installed:${N} ${DONE[*]:-none}"
say "already:   ${SKIPPED[*]:-none}"
if [[ ${#FAILED[@]} -gt 0 ]]; then say "${R}failed:${N}    ${FAILED[*]}"; rc=1; fi
if [[ $DRY == 0 ]]; then
  say ""
  say "Next: open a folder from Ubuntu with 'code .' (the first time VS Code installs its WSL server), then run"
  say "'Developer: Reload Window' once. Sign in from inside VS Code to: Claude Code, GitHub (pull requests, Actions), Azure."
  say "For the terminal_font setting, install a Nerd Font on Windows (from WSL, no PowerShell needed): winget.exe install DEVCOM.JetBrainsMonoNerdFont"
fi
exit $rc
