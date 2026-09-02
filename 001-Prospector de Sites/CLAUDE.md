# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo has two distinct halves that must not be confused:

1. **`PROSPECTOR-DE-SITES/`** — the source of a Claude Code/Cowork **plugin** ("Prospector de Sites", by Helio Arreche) distributed via a plugin marketplace (`.claude-plugin/marketplace.json`). This is the code you edit when asked to change plugin behavior (commands, skills, templates, hooks).
2. **`Clientes/`** — a live **"pasta conectada"** (connected folder): the runtime data produced by *using* the plugin for a real prospecting business (Kairós TecnologIA). It contains the SQLite lead database, generated client sites, the dashboard, and business documents. Most of this is business data, not source code — edit it only when the user is actually operating the business workflow (e.g. fixing a generated site, tweaking the dashboard template), not when doing generic "plugin development."

The plugin's own `README.md` and `prospector-de-sites/README.md` describe the installable product; `Clientes/` is one operator's actual instance of it (this is why files under `Clientes/sites/*` and `Clientes/Antigos e backups/` look like generated/backup artifacts rather than hand-written code).

## The plugin's workflow (mental model)

The whole plugin implements one pipeline, one slash command per stage, always in this order:

```
/setup → /prospectar → /redesenhar → /editor (optional) → /publicar → /proposta → /respostas → /followup → /contrato
```

- `/setup` — one-time config: signature, default niches, location (country/state/city — also drives `google_gl`/`google_hl`), HostGator credentials (password is filled by the user only via the dashboard's Settings tab or by hand-editing `prospector-config.json`, never typed in chat), and bootstraps the dashboard.
- `/prospectar` — scrapes Google Maps (via Claude in Chrome) for well-rated businesses with a weak/missing site, dedupes against `prospector.db`, writes leads to a Google Sheet + local `leads.md` + dashboard.
- `/redesenhar` — rewrites each lead's site as a premium single-file HTML page (never touches real facts, but rewrites copy), always produces a matching `-editor.html` and updates root `comparar.html`.
- `/editor` — regenerates just the `-editor.html` visual editor for one client.
- `/publicar` — uploads to HostGator (`public_html/[pastaBase]/[slug]/`) and verifies HTTPS.
- `/proposta` — drafts (default) or sends the outreach email/WhatsApp message via Gmail, must pass an anti-spam checklist.
- `/respostas` — checks Gmail for replies and updates lead status; never auto-marks `fechado`.
- `/followup` — one polite follow-up per lead after 3+ days of silence.
- `/contrato` — generates the service contract (HTML + locked DOCX) once a deal closes.

Command specs live in `PROSPECTOR-DE-SITES/prospector-de-sites/commands/*.md`; the actual how-to detail each command delegates to is in the matching skill under `PROSPECTOR-DE-SITES/prospector-de-sites/skills/<skill>/SKILL.md` (with supporting files in that skill's `references/`). **Always read the relevant SKILL.md before touching the workflow it governs** — the commands are intentionally thin and point to the skill as the source of truth.

Skill ↔ command mapping:

| Skill | Used by |
|---|---|
| `prospeccao-maps` | `/prospectar` |
| `redesign-premium` | `/redesenhar`, `/editor` |
| `deploy-hostgator` | `/publicar`, `/setup` connection test |
| `proposta-email` | `/proposta`, `/followup` |
| `dashboard-leads` | every command that mutates lead data |
| `contrato-servico` | `/contrato` |

## The slug: single most important invariant

Every lead gets a `slug` (slugified business name, no niche prefix) **once**, at creation time in `/prospectar`. It becomes the SQLite primary key, the folder name (`sites/bh/oficinas/<slug>/`), every filename (`<slug>.html`, `<slug>-editor.html`, `proposta.html`, `contrato-<slug>...`), and the public URL path. It is **immutable** — every later command must read it back out of `prospector.db` (matched by `nome`) and reuse it verbatim, never re-derive it from the name. Slug generation rule (Python, in `dashboard-leads/SKILL.md`):

```python
import re, unicodedata
def slugify(nome):
    s = unicodedata.normalize('NFKD', nome).encode('ascii','ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+','-', s).strip('-').lower()
    return re.sub(r'-{2,}','-', s)
```

If a folder/file name and the DB slug ever diverge, the dashboard's "página"/"editar site" buttons break — treat any mismatch as a bug to fix before proceeding, not something to paper over.

## Dashboard architecture (`prospector.db` + `dashboard-server.py` + `dashboard.html`)

- **`prospector.db`** (SQLite, single table `leads`, PK `slug`) is the source of truth for all lead/client state. Schema and status lifecycle (`novo → redesenhado → publicado → proposta → respondeu → fechado`, plus `descartado`) are defined in `dashboard-leads/SKILL.md`.
- **`dashboard-server.py`** is a dependency-free stdlib `http.server` app (no Flask/etc). Routes: `GET /api/config` (strips the HostGator password before returning), `GET /api/leads`, `POST /api/leads` (insert/replace), `PUT /api/config`, `PUT /api/leads/<slug>` (partial update), `DELETE /api/leads/<slug>`. Serves `dashboard.html` at `/`. Run with `python dashboard-server.py` (or double-click `iniciar-dashboard.bat`), listens on `http://localhost:8765`.
- **`dashboard.html`** is generated from a template with a `<script id="dados" type="application/json">{"leads": [...]}</script>` snapshot embedded, so it also works read-only when opened as a plain file (no server). On first server run with no `prospector.db`, `importar_snapshot()` seeds the DB from that embedded JSON.
- Every command that mutates leads must do BOTH: upsert into `prospector.db`, then regenerate `dashboard.html`'s embedded snapshot. Never implement kanban/funnel/financials UI logic outside the template — the skill explicitly says the dashboard template already does this.

## Deploying to HostGator (no direct network access)

The Cowork/Code sandbox generally **cannot reach FTP or cPanel directly**, so publishing is **manual and user-driven**. `deploy-hostgator/SKILL.md` details it:

1. **Default (manual publisher):** write `fila-publicacao.txt` (queue file, `local/path|remote/path` per line) into the connected folder, then **ask the user to run `publicar-agora.bat`** (Windows) / `publicar-agora.command` (Mac). It uploads the queue and renames it to `fila-publicada-[date].txt` (log in `publicador-log.txt`). **Never publish automatically or rely on a background/scheduled poller — after writing the queue, ALWAYS wait for the user to run the publisher and confirm before verifying URLs.** (The old auto scheduled task `ProspectorPublicador` is deprecated; remove it with `schtasks /Delete /TN ProspectorPublicador /F`.)
2. Only if the user explicitly asks: try a silent `curl` FTP upload from the sandbox (usually blocked).
3. Last resort: drive the cPanel File Manager via Claude in Chrome with the user logged in themselves.

The cPanel password lives only in `prospector-config.json` on the user's machine — never print, log, or ask for it in chat. HTTPS on the published URL is a blocking requirement before considering a publish complete.

## Secrets and data boundaries

- `prospector-config.json` holds HostGator credentials in plaintext locally; `.gitignore` excludes `*.db`, `.env`, `credentials.json`, `*.key` — don't defeat that by committing generated DB/backup files.
- The `Antigos e backups/` folders under `Clientes/` are timestamped manual backups (`*-YYYYMMDD-HHMMSS*`) — treat them as historical snapshots, not files to edit.
- Generated client sites (`Clientes/sites/bh/oficinas/<slug>/*.html`) are self-contained single-file HTML (inline CSS, base64 images, no build step) — edit them directly with the visual editor conventions described in `redesign-premium/references/editor-visual.md`, not via a bundler.
