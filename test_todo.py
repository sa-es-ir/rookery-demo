from todo import add, done, show


def test_add_and_done():
    tasks = add([], "write docs")
    tasks = add(tasks, "ship it")
    tasks = done(tasks, 1)
    assert show(tasks) == "1. [x] write docs\n2. [ ] ship it"


if __name__ == "__main__":
    test_add_and_done()
    print("ok")
