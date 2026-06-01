---
name: feedback-approach
description: User preferences for how to collaborate — what to do and not do
metadata:
  type: feedback
---

User prefers to run commands themselves (pip install, git commit, etc.) — offer the command, don't execute it unless asked.

**Why:** They said "I'll do it" when offered pip install, and committed to git themselves without asking.

**How to apply:** For terminal operations that affect the user's environment or repo state (installs, commits, pushes), write the command as a code block and let them run it. Only execute via Bash when they explicitly ask to "try it out" or "run it."

---

Starlette 1.2.1 (installed in this project's venv) changed `TemplateResponse` API: `request` is now the first positional arg, not part of the context dict.

**Old (broken):** `templates.TemplateResponse("name.html", {"request": request, ...})`
**New (correct):** `templates.TemplateResponse(request, "name.html", {...})`

**Why:** Breaking change in Starlette 1.x. The old call puts the template name in the `request` slot and the dict in the `name` slot — Jinja2 then tries to hash a dict as a cache key and raises `TypeError: unhashable type: 'dict'`.

**How to apply:** Any new FastAPI route in this project must use the new call signature.
