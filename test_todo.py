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


if __name__ == "__main__":
    test_add_and_done()
    test_add_due()
    print("ok")
