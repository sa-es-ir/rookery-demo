"""A tiny to-do list for the terminal. Tasks live in todo.json next to where you run it."""
import argparse
import json
from pathlib import Path

FILE = Path("todo.json")


def load():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def save(tasks):
    FILE.write_text(json.dumps(tasks, indent=2))


def add(tasks, text):
    tasks.append({"text": text, "done": False})
    return tasks


def done(tasks, n):
    tasks[n - 1]["done"] = True
    return tasks


def clear(tasks):
    for t in tasks:
        if t["done"]:
            tasks.remove(t)
    return tasks


def show(tasks):
    return "\n".join(f"{i}. [{'x' if t['done'] else ' '}] {t['text']}" for i, t in enumerate(tasks, 1))


def main(argv=None):
    p = argparse.ArgumentParser(prog="todo")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("add").add_argument("text")
    sub.add_parser("done").add_argument("n", type=int)
    sub.add_parser("list")
    sub.add_parser("clear")
    a = p.parse_args(argv)
    tasks = load()
    if a.cmd == "add":
        save(add(tasks, a.text))
    elif a.cmd == "done":
        save(done(tasks, a.n))
    elif a.cmd == "clear":
        save(clear(tasks))
    print(show(load()))


if __name__ == "__main__":
    main()
