import tempfile
from datetime import date
from pathlib import Path

import todo
from todo import add, done, show


def test_add_and_done():
    tasks = add([], "write docs")
    tasks = add(tasks, "ship it")
    tasks = done(tasks, 1)
    assert show(tasks) == "1. [x] write docs\n2. [ ] ship it"


def test_add_due():
    tasks = add([], "x", "2026-11-01")
    assert tasks == [{"text": "x", "done": False, "due": "2026-11-01"}]
    for bad in ("11/01/2026", "2026-02-30"):
        try:
            add([], "x", bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")


def test_show_due():
    today = date(2026, 10, 17)
    assert show(add([], "x", "2026-11-01"), today=today) == "1. [ ] x (due 2026-11-01)"


def test_show_overdue():
    today = date(2026, 10, 17)
    assert show(add([], "x", "2026-10-01"), today=today) == "1. [ ] x (due 2026-10-01) OVERDUE"


def test_show_done_past_due_not_overdue():
    today = date(2026, 10, 17)
    tasks = done(add([], "x", "2026-10-01"), 1)
    assert show(tasks, today=today) == "1. [x] x (due 2026-10-01)"


def test_show_due_today_not_overdue():
    today = date(2026, 10, 17)
    assert show(add([], "x", "2026-10-17"), today=today) == "1. [ ] x (due 2026-10-17)"


def test_main_bad_due_exits_2_and_saves_nothing():
    original = todo.FILE
    with tempfile.TemporaryDirectory() as d:
        todo.FILE = Path(d) / "todo.json"
        try:
            todo.main(["add", "x", "--due", "not-a-date"])
        except SystemExit as e:
            assert e.code == 2
        else:
            raise AssertionError("expected SystemExit")
        finally:
            todo.FILE = original
        assert not Path(d, "todo.json").exists()


if __name__ == "__main__":
    test_add_and_done()
    test_add_due()
    test_show_due()
    test_show_overdue()
    test_show_done_past_due_not_overdue()
    test_show_due_today_not_overdue()
    test_main_bad_due_exits_2_and_saves_nothing()
    print("ok")
