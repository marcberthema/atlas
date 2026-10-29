#!/usr/bin/env python3
"""Claude Code status line: reads the session JSON on stdin, prints one line.

  Opus 5.5 · high · ~/src/atlas · main* · ▓▓▓░░░░░░░ 62K/200K · 5h 23% (2h14m) · 7d 41% (Mon 14:00) · $1.84

The bar and the percentages are green under 50%, yellow under 80%, red from 80%. The last figure is the session cost, then the
cost of the week: Claude Code only sends the session's cost, so each run adds the growth since the last run to a ledger,
~/.claude/statusline-cost.json, and sums the entries inside the 7-day window (the same reset as the 7d figure). It counts from
the first run, on this machine only. Costs are estimates at list price, not a bill.

Fields are documented at https://code.claude.com/docs/en/statusline. A field Claude Code does not send (effort on a model
without it, rate limits outside Pro and Max or before the first reply) is left out. Python 3 standard library only.
setup.sh copies it to ~/.claude/statusline.py and points settings.json at it.
"""
import fcntl
import json
import os
import subprocess
import sys
import time

RESET, DIM = "\033[0m", "\033[2m"
GREEN, YELLOW, RED, CYAN, MAGENTA = "\033[32m", "\033[33m", "\033[31m", "\033[36m", "\033[35m"


def level(pct):
    """Green under 50%, yellow under 80%, red from 80%."""
    return GREEN if pct < 50 else YELLOW if pct < 80 else RED


def bar(pct, width=10):
    full = round(pct / 100 * width)
    return "▓" * full + "░" * (width - full)


def tokens(n):
    """62000 -> 62K, 1000000 -> 1M."""
    return f"{n / 1_000_000:g}M" if n >= 1_000_000 else f"{n / 1000:.0f}K"


def until(epoch):
    """Time left before a reset: 2h14m under a day, the weekday and hour beyond."""
    left = int(epoch - time.time())
    if left <= 0:
        return "now"
    if left < 86400:
        return f"{left // 3600}h{left % 3600 // 60:02d}m" if left >= 3600 else f"{left // 60}m"
    return time.strftime("%a %H:%M", time.localtime(epoch))


def git_branch(cwd):
    """Branch name, with * when the work tree has changes. None outside a repository."""
    try:
        run = lambda *a: subprocess.run(["git", "-C", cwd, *a], capture_output=True, text=True, timeout=1)
        b = run("branch", "--show-current")
        if b.returncode:
            return None
        name = b.stdout.strip() or run("rev-parse", "--short", "HEAD").stdout.strip()
        dirty = run("status", "--porcelain", "--untracked-files=no").stdout.strip()
        return name + ("*" if dirty else "")
    except (OSError, subprocess.TimeoutExpired):
        return None


WEEK = 7 * 86400


def week_cost(d, window_start):
    """Record how much this session's cost grew since the last run and return the cost of the window. None when it cannot be kept."""
    path = os.environ.get("CLAUDE_STATUSLINE_LEDGER") or os.path.expanduser("~/.claude/statusline-cost.json")
    try:
        with open(path + ".lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)   # several sessions can run this at once
            try:
                ledger = json.load(open(path))
            except (OSError, ValueError):
                ledger = {}
            sessions, entries = ledger.get("sessions", {}), ledger.get("entries", [])
            now, sid = time.time(), d.get("session_id")
            cost = d.get("cost", {}).get("total_cost_usd")
            if sid and cost is not None:
                seen = sessions.get(sid)
                if seen is None:
                    # first sight: count the spend so far only if the session is young enough to have started inside the window
                    age = d.get("cost", {}).get("total_duration_ms", 0) / 1000
                    delta = cost if now - age >= window_start else 0
                else:
                    delta = cost - seen["last"] if cost >= seen["last"] else cost   # a lower cost means it was reset
                if delta > 0:
                    entries.append([now, round(delta, 4)])
                sessions[sid] = {"last": cost, "seen": now}
            entries = [e for e in entries if e[0] >= now - WEEK - 86400]
            sessions = {k: v for k, v in sessions.items() if v["seen"] >= now - WEEK - 86400}
            tmp = path + ".tmp"
            with open(tmp, "w") as f:
                json.dump({"sessions": sessions, "entries": entries}, f)
            os.replace(tmp, path)
            return sum(delta for ts, delta in entries if ts >= window_start)
    except OSError:
        return None


def main():
    d = json.load(sys.stdin)
    sep = f" {DIM}·{RESET} "

    cwd = d.get("workspace", {}).get("current_dir") or d.get("cwd") or os.getcwd()
    parts = [f"{CYAN}{d.get('model', {}).get('display_name', '?')}{RESET}"]
    if d.get("effort", {}).get("level"):
        parts.append(f"{MAGENTA}{d['effort']['level']}{RESET}")
    if d.get("fast_mode"):
        parts.append(f"{YELLOW}fast{RESET}")
    home = os.path.expanduser("~")
    parts.append(cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd)
    branch = git_branch(cwd)
    if branch:
        parts.append(f"{GREEN}{branch}{RESET}")

    cw = d.get("context_window", {})
    ctx = cw.get("used_percentage")
    if ctx is not None:
        size = cw.get("context_window_size")
        used = cw.get("total_input_tokens")   # the same input-only sum the percentage is calculated from
        label = f"{tokens(used)}/{tokens(size)}" if used is not None and size else f"{ctx:.0f}%"
        parts.append(f"{level(ctx)}{bar(ctx)} {label}{RESET}")
    limits = d.get("rate_limits") or {}
    for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
        w = limits.get(key)
        if w and w.get("used_percentage") is not None:
            pct = w["used_percentage"]
            reset = f" {DIM}({until(w['resets_at'])}){RESET}" if w.get("resets_at") else ""
            parts.append(f"{label} {level(pct)}{pct:.0f}%{RESET}{reset}")
    cost = d.get("cost", {}).get("total_cost_usd")
    reset = (limits.get("seven_day") or {}).get("resets_at")
    week = week_cost(d, reset - WEEK if reset else time.time() - WEEK)
    if cost or week:
        parts.append(f"{DIM}${cost or 0:.2f}" + (f" · ${week:.0f} wk" if week else "") + RESET)

    print(sep.join(parts))


if __name__ == "__main__":
    main()
