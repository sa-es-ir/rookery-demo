"""A tiny to-do list for the terminal. Tasks live in todo.json next to where you run it."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

FILE = Path("todo.json")
DUE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


def load():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def save(tasks):
    FILE.write_text(json.dumps(tasks, indent=2))


def parse_due(value):
    if not DUE_RE.fullmatch(value):
        raise ValueError("due date must be YYYY-MM-DD")
    date.fromisoformat(value)
    return value


def add(tasks, text, due=None):
    if due is None:
        tasks.append({"text": text, "done": False})
    else:
        tasks.append({"text": text, "done": False, "due": parse_due(due)})
    return tasks


def done(tasks, n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"task number must be an int, not {type(n).__name__}")
    if not 1 <= n <= len(tasks):
        raise IndexError(n)
    tasks[n - 1]["done"] = True
    return tasks


def remove(tasks, n):
    if not 1 <= n <= len(tasks):
        raise IndexError(n)
    del tasks[n - 1]
    return tasks


def show(tasks, today=None):
    today = today or date.today()
    lines = []
    for i, t in enumerate(tasks, 1):
        line = f"{i}. [{'x' if t['done'] else ' '}] {t['text']}"
        due = t.get("due")
        if due:
            line += f" (due {due})"
            if not t["done"] and date.fromisoformat(due) < today:
                line += " OVERDUE"
        lines.append(line)
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(prog="todo")
    sub = p.add_subparsers(dest="cmd", required=True)
    add_p = sub.add_parser("add")
    add_p.add_argument("text")
    add_p.add_argument("--due")
    sub.add_parser("done").add_argument("n", type=int)
    sub.add_parser("remove").add_argument("n", type=int)
    sub.add_parser("list")
    a = p.parse_args(argv)
    tasks = load()
    if a.cmd == "add":
        try:
            save(add(tasks, a.text, a.due))
        except ValueError as e:
            print(f"todo: error: {e}", file=sys.stderr)
            sys.exit(2)
    elif a.cmd == "done":
        try:
            save(done(tasks, a.n))
        except IndexError:
            print(f"todo: error: no task {a.n}", file=sys.stderr)
            sys.exit(2)
    elif a.cmd == "remove":
        try:
            save(remove(tasks, a.n))
        except IndexError:
            print(f"todo: error: no task {a.n}", file=sys.stderr)
            sys.exit(2)
    print(show(load()))


if __name__ == "__main__":
    main()
