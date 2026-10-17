from todo import add, clear, done, show


def test_add_and_done():
    tasks = add([], "write docs")
    tasks = add(tasks, "ship it")
    tasks = done(tasks, 1)
    assert show(tasks) == "1. [x] write docs\n2. [ ] ship it"


def test_clear():
    tasks = add(add([], "a"), "b")
    tasks = clear(done(tasks, 1))
    assert show(tasks) == "1. [ ] b"


if __name__ == "__main__":
    test_add_and_done()
    test_clear()
    print("ok")
