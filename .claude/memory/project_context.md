---
name: project-context
description: Context about the lead management tool being built for the Israeli scientific equipment business
metadata: 
  node_type: memory
  type: project
  originSessionId: e207d8a4-c203-4833-ab6d-a19710a513c1
---

**Status: Complete and committed to git (June 2026).**

Local Python/FastAPI lead management & outreach tool for a small Israeli business that sells/services scientific analytical equipment (spectrometers, UV analysers, gas analysers, pharma dissolution/diffusion testers, etc.).

**Why:** Business is in financial distress (June 2026, only 1 order all year). They shut down their website to cut costs. They rely on 3–4 repeat clients and do little outreach.

**How to apply:** The goal is zero ongoing cost — everything runs locally (`python run.py`). No hosting, no cloud services.

Project lives at: `/home/Michael/projects/work_help/lead_manager/`

**Stack:** Python + FastAPI + SQLite (SQLAlchemy) + Jinja2 + Tailwind CSS (CDN)

**Key assets:**
- Exhibition Excel leads (~2 years old) — import as "dormant" status
- Small existing client list that can be compiled
- Owner is fairly technical

**What was built:**
- `run.py` — starts server + opens browser
- `app/main.py` — all FastAPI routes
- `app/models.py` — Lead + ContactLog ORM models
- `app/crud.py` — all DB operations including bulk import with dedup
- `app/templates/` — dashboard, leads list, lead detail, import flow (Excel/CSV with column mapping), email/call templates (Hebrew + English), discovery guide
