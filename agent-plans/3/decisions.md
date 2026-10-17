# Decisions — issue #3

- Tests use plain `try/except/else` to assert `ValueError` instead of pytest, since the project is stdlib-only and run as `python test_todo.py`.
- `parse_due` lets `date.fromisoformat`'s own `ValueError` propagate unwrapped for impossible dates (e.g. `2026-02-30`); callers only need to catch `ValueError`.
- `add()` keeps the exact two-key dict when `due is None`, so existing tasks/serialized data are unchanged.
- The box has no `python` on PATH; tests were run as `python3 test_todo.py`.
- `show()` treats a falsy `due` (missing or empty) as absent, and appends `" OVERDUE"` only after the `(due ...)` suffix so the plan's example line format holds exactly.
- The `main` test monkeypatches `todo.FILE` to a path under `tempfile.TemporaryDirectory` and restores the original module attribute in a `finally`, so no test leaks state into later tests; it calls the real `todo.main` rather than a copied CLI path.
- Manual verification ran in a temporary cwd using the absolute path to `todo.py`, so the worktree gained no `todo.json` side effect.
