# Decisions — issue #3

- Tests use plain `try/except/else` to assert `ValueError` instead of pytest, since the project is stdlib-only and run as `python test_todo.py`.
- `parse_due` lets `date.fromisoformat`'s own `ValueError` propagate unwrapped for impossible dates (e.g. `2026-02-30`); callers only need to catch `ValueError`.
- `add()` keeps the exact two-key dict when `due is None`, so existing tasks/serialized data are unchanged.
- The box has no `python` on PATH; tests were run as `python3 test_todo.py`.
