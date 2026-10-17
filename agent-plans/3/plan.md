# Plan: Add due dates to tasks

## Goal
`todo.py add` accepts an optional `--due YYYY-MM-DD`; `list` shows the due date
after the text and marks not-done, past-due tasks `OVERDUE`; an invalid date is
an error that saves nothing; tasks saved without a date keep working.

## Approach
All changes are in `todo.py` and `test_todo.py` (plain asserts, run with
`python test_todo.py`).

1. **Data model.** A task stays a dict. New tasks with a due date get an extra
   key `"due"` holding the validated string (e.g. `"2026-11-01"`). Existing
   tasks have no `"due"` key; every read uses `t.get("due")` so they keep
   working. `done()` is unchanged — it only sets `done`, so a `due` key is
   preserved.

2. **Validation.** Add a module-level `DUE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")`
   and a `parse_due(value)` helper that (a) rejects anything not matching
   `DUE_RE.fullmatch`, then (b) calls `datetime.date.fromisoformat(value)` so
   impossible dates like `2026-02-30` are also rejected. It returns the
   validated string or raises `ValueError`. `add()` gains an optional third
   parameter `due=None`; when it is not `None`, `add()` calls `parse_due(due)`
   and stores `{"text": text, "done": False, "due": due}` (otherwise it stores
   the existing two-key dict).

3. **Rendering.** `show(tasks, today=None)` resolves `today = today or date.today()`
   (the parameter is a test seam; real callers pass nothing). For each task it
   builds `"{i}. [{'x' if done else ' '}] {text}"`, appends `" (due {due})"` when
   a due date exists, and appends `" OVERDUE"` only when the task is not done
   and `date.fromisoformat(due) < today` (strictly past; a task due today is not
   overdue).

4. **CLI.** The `add` subparser adds `--due`. In `main`, the `add` branch calls
   `add(tasks, a.text, a.due)` inside `try/except ValueError`; on `ValueError`
   it prints `todo: error: {message}` to stderr and exits with code 2, so
   nothing is saved. `todo.py` gains `import re`, `import sys`, and
   `from datetime import date`.

## Decisions
- **Store `due` as the validated string**, not a `date` object — JSON in
  `todo.json` cannot round-trip `date`, and string storage keeps `save()`/
  `load()` unchanged.
- **`OVERDUE` placement:** appended at the very end of the line, after the
  `(due ...)` suffix, e.g. `1. [ ] renew passport (due 2026-10-01) OVERDUE`.
- **"Passed" is strictly `< today`**, so a task due today is not overdue.
- **`show()` takes an optional `today` argument** (defaults to real today) so
  overdue behaviour is testable without depending on the wall clock.
- **Invalid-date failure is exit code 2** with the message on stderr, matching
  argparse's own error convention, and it happens before `save()` so no write
  occurs.

## Assumptions
- The exact `OVERDUE` line format is not specified in the issue; I chose
  `... (due YYYY-MM-DD) OVERDUE` as the least surprising reading of "marked
  `OVERDUE`".
- Error text: `todo: error: due date must be YYYY-MM-DD` (or the specific
  `ValueError` message from `parse_due`). The precise wording is not part of the
  acceptance criteria.
- A task with a hand-edited, malformed `due` in `todo.json` is out of scope;
  only newly added dates are validated.

## Out of scope
- No editing/removing due dates (no `--due` on `done`, no clear command).
- No sorting by due date, no relative dates, no recurring tasks.
- No changes to `README.md`, CI, or any file other than `todo.py` and
  `test_todo.py`.

## How to verify
- `python test_todo.py` — prints `ok` and exits 0.
- `python todo.py add "renew passport" --due 2026-11-01` — prints the list with
  `1. [ ] renew passport (due 2026-11-01)`.
- `python todo.py add "bad" --due 11/01/2026` — prints an error and does not
  add the task (check `todo.json` is unchanged / `list` does not show it).

Owner: heron
