import contextlib
import io
import json
import tempfile
from datetime import date
from pathlib import Path

import todo
from todo import add, done, remove, show


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


def test_remove():
    tasks = add(add(add([], "a"), "b"), "c")
    remove(tasks, 2)
    assert show(tasks) == "1. [ ] a\n2. [ ] c"


def test_remove_out_of_range():
    tasks = add(add([], "a"), "b")
    for n in (0, 3):
        try:
            remove(tasks, n)
        except IndexError:
            pass
        else:
            raise AssertionError(f"expected IndexError for {n}")
    assert show(tasks) == "1. [ ] a\n2. [ ] b"


def test_done_out_of_range():
    tasks = add(add([], "a"), "b")
    for n in (0, 3):
        try:
            done(tasks, n)
        except IndexError:
            pass
        else:
            raise AssertionError(f"expected IndexError for {n}")
    assert show(tasks) == "1. [ ] a\n2. [ ] b"


def test_done_rejects_non_int():
    tasks = add([], "a")
    for n in (True, "1", 1.0):
        try:
            done(tasks, n)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for {n!r}")
    assert show(tasks) == "1. [ ] a"


def test_main_done_out_of_range_exits_2_and_saves_nothing():
    original = todo.FILE
    with tempfile.TemporaryDirectory() as d:
        todo.FILE = Path(d) / "todo.json"
        err = io.StringIO()
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                todo.main(["done", "0"])
        except SystemExit as e:
            assert e.code == 2
        else:
            raise AssertionError("expected SystemExit")
        finally:
            todo.FILE = original
        assert not Path(d, "todo.json").exists()
        assert err.getvalue().strip() == "todo: error: no task 0"


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


def test_main_remove_out_of_range_exits_2_and_saves_nothing():
    original = todo.FILE
    with tempfile.TemporaryDirectory() as d:
        todo.FILE = Path(d) / "todo.json"
        err = io.StringIO()
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                todo.main(["remove", "9"])
        except SystemExit as e:
            assert e.code == 2
        else:
            raise AssertionError("expected SystemExit")
        finally:
            todo.FILE = original
        assert not Path(d, "todo.json").exists()
        assert err.getvalue().strip() == "todo: error: no task 9"


def test_main_remove_saves():
    original = todo.FILE
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "todo.json"
        todo.FILE = path
        todo.save(todo.add(todo.add([], "a"), "b"))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                todo.main(["remove", "1"])
        finally:
            todo.FILE = original
        assert json.loads(path.read_text()) == [{"text": "b", "done": False}]


if __name__ == "__main__":
    test_add_and_done()
    test_add_due()
    test_show_due()
    test_show_overdue()
    test_show_done_past_due_not_overdue()
    test_show_due_today_not_overdue()
    test_remove()
    test_remove_out_of_range()
    test_done_out_of_range()
    test_done_rejects_non_int()
    test_main_done_out_of_range_exits_2_and_saves_nothing()
    test_main_bad_due_exits_2_and_saves_nothing()
    test_main_remove_out_of_range_exits_2_and_saves_nothing()
    test_main_remove_saves()
    print("ok")
