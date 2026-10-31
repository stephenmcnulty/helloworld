# Journal Entry Prep (demo)

An internal web tool that walks a preparer from a **payroll register** (CSV/Excel) to an **import-ready journal entry file** for **Sage Intacct** or **QuickBooks Online** - with mapping review, validation, a second-person approval, and an audit trail.

> **This is a demo.** It uses only synthetic data, shows a "DEMO - synthetic data only" banner, and **never posts anything to Intacct or QuickBooks** - it only produces a CSV that a person imports themselves. It is structured so it could become a production tool; see [What would be needed for production](#what-would-be-needed-for-production).

## Quick start

Requires Python 3.11+.

```bash
cd jeprep
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
./run_demo.sh            # http://127.0.0.1:8000  (sets DEMO_MODE=true)
```

Open <http://127.0.0.1:8000>, enter a name, email and role on the sign-in form (the page has one-click links that pre-fill the demo people), and follow the [demo script](#demo-script). No account and no API key are needed. To start over, stop the server and delete the `data/` folder.

```bash
python -m pytest         # ~215 tests: validation, allocation math, export formats, redaction, security, end-to-end flows
```

## Demo script

On the sign-in page, the *Fill in the form as a demo person* links pre-fill the name, email and role below (you still press Continue). Sample files live in `demo_data/` (and are offered as downloads on the Upload step in demo mode). Everything - clients, names, IDs, amounts - is randomly generated.

| # | Fill in the sign-in form as | Do this | What it shows |
|---|---|---|---|
| 1 | **Pat Preparer** (Preparer) | New journal entry → *Our Lady of Grace*, Intacct, 10/01-10/15/2026, **allocate: Yes** → upload `our-lady-grace_payroll_2026-10-15.csv` | Layout is **detected** as matching saved mapping **v2**; goes straight to preview. Allocation splits expense 60/30/10 Parish/School/Gift Store and adds due-to/due-from lines; every entity balances. |
| 2 | Pat | Preview → **Request export approval** | Five checks, all with plain-language results. |
| 3 | Pat | Try approving it | Not possible: Preparers have no approve button; the server refuses too. |
| 4 | **Rhea Reviewer** (Reviewer) | Review queue → open → **Approve export** | Second-person approval. |
| 5 | Pat | Export → generate (leave *delete source file after export* ticked) → download | Intacct CSV; the uploaded source file is deleted. |
| 6 | **Rhea as Reviewer** | Start a *St. Brigid* job (QBO) with `st-brigid_payroll_2026-10-15.csv`, submit the rules-proposed mapping, have **Sam Senior** approve it, request export, then try to approve it yourself as Rhea | **"A user cannot approve their own export"** - refused, and the refusal is logged. |
| 7 | Pat | New job → *Our Lady of Grace*, 10/16-10/31/2026 → upload `..._NEW-LAYOUT.csv` | A new payroll provider's column names: **no saved mapping matches**. Only the employee ID / department / date columns are recognised by rules. |
| 8 | Pat | **Suggest a mapping** → open *Show exactly what would be sent to the model* | Offline this is a clearly labelled **MOCK**; with `ANTHROPIC_API_KEY` it calls Claude. The panel shows names/IDs replaced by `EMP_001` / `ID_001`. The suggestion spots `Total Earnings` as a subtotal and sets it to *Ignore* (posting it would double count). Nothing is applied: each AI/mock line must be ticked *Reviewed*, then submitted. |
| 9 | **Sam Senior** (Reviewer) | Review queue → approve the mapping | Saved as **version 3**. Re-uploading the same layout now matches it automatically. |
| 10 | Pat | New job → `..._BROKEN.csv` (10/01-10/15) | Four checks **fail**: out of balance overall and for the entity (the $25), doesn't tie to the report's own totals, and a row dated 09/30. **Export is blocked.** |
| 11 | **Alex Admin** (Admin) | Audit log; Clients → edit allocation % | Who/what/when, mapping version, file SHA-256, approver; hash chain verified. Percent changes are logged and drive the next allocated journal. |

## How it works

### The five steps
1. **Intake** - client, target system (Sage Intacct / QuickBooks Online), report type (Payroll Register), pay period, allocate yes/no.
2. **Upload** - CSV or Excel. The file is validated, stored privately, hashed, and its column layout is fingerprinted. If an **approved mapping for that client + report type has the same layout**, it is used; otherwise the job is routed to mapping.
3. **Mapping review** - every report column next to its role, side (debit/credit), GL account, optional offset account, entity and fund. Edit, then **submit**; a **Reviewer** approves it. Approved mappings are immutable, numbered versions per client + report type.
4. **Preview** - draft journal, tie-out table, balance by entity, and these checks (export is blocked if any **fail**):
   1. **No unmapped lines** - every column has a role; every posting line has a valid account, entity and fund from the client's lists.
   2. **Debits equal credits.**
   3. **Each entity balances on its own** (this is what makes allocation correct).
   4. **Totals tie back to the source report** - per column: sum of rows vs the report's own total row vs the amount in the journal.
   5. **Dates fall within the selected pay period** - journal date and every row's pay date.
5. **Export** - a Reviewer other than the preparer approves; then the import CSV is generated (and, optionally, the source upload deleted). The approval is bound to a hash of the exact journal content, so a changed journal can't ride on an old approval.

### Mapping engine
* **Rules** (`app/rules.py`) - deterministic header patterns for common payroll columns (gross, employer taxes, withholdings, net pay ...). Same input, same output. They *propose*; they never approve.
* **Saved mappings** - exact layout match → the approved version is used. A changed layout that shares columns with a saved mapping reuses those columns in a new draft.
* **`suggest_mapping()`** (`app/suggest.py`) - for unfamiliar layouts. Uses the Claude API when `ANTHROPIC_API_KEY` is set (default model `claude-opus-5-5`, override with `ANTHROPIC_MODEL`); otherwise - or if the call fails or is refused - falls back to a **mock** keyword heuristic that is labelled as such everywhere. Model output is validated against the client's real chart of accounts, entities and funds before it is shown; invalid values are cleared, not trusted.
* **Redaction** (`app/redaction.py`) - before any model call, employee names and ID numbers (including SSN-shaped numbers, emails, name/ID columns detected by header, and high-cardinality free text) become tokens (`EMP_001`, `ID_001` ...). Only headers, the row count and up to 3 redacted sample rows are sent. The token map lives in memory for the one request and is used to restore real values in the model's answer. Tests assert that no real name/ID appears in the outgoing request.
* **Never auto-applied** - a suggestion only fills columns that are still unassigned, is flagged AI/MOCK, requires a per-line *Reviewed* tick, and still needs a different Reviewer's approval.

### Allocation
For clients with several entities (e.g. Parish / School / Gift Store), expense lines are split by the client's percentages using the **largest-remainder method in whole cents** (parts always add up exactly). Each split line uses the entity's default fund. The **paying entity** keeps cash and liabilities; every other entity gets a **Due to <payer>** credit and the payer gets a matching **Due from <entity>** debit, so each entity balances on its own. Percentages are managed by an Admin.

### Roles
| Role | Can |
|---|---|
| **Preparer** | Run the wizard, propose/edit mappings, request export approval |
| **Reviewer** | Everything a Preparer can, plus approve mappings and exports - **never ones they prepared** |
| **Admin** | Manage clients/allocation, view the audit log, run the retention purge. (Does not prepare journals.) |

Permissions are enforced on the server for every route; hiding a button is never the only control. Segregation of duties applies to exports *and* mappings, keyed on the user's identity (email), so changing role mid-demo doesn't get around it.

### Export formats (`app/exporters.py`)
* **Sage Intacct** GL journal import: `DONOTIMPORT, JOURNAL, DATE, REVERSEDATE, DESCRIPTION, REFERENCE_NO, LINE_NO, ACCT_NO, LOCATION_ID, DEPT_ID, CLASSID, DOCUMENT, MEMO, DEBIT, CREDIT, SOURCEENTITY, CURRENCY, STATE` - entity → `LOCATION_ID`, fund → `CLASSID`.
* **QuickBooks Online** journal entry import: `JournalNo, JournalDate, Currency, Memo, Account, Debits, Credits, Description, Name, Location, Class` - entity → `Location`, fund → `Class`, account written as `"<number> <name>"`.

**These layouts are my best reconstruction of the standard templates, not verified against a live tenant.** Before real use, diff them against a template downloaded from the client's own Intacct/QBO company (custom dimensions, the journal symbol `GJ`, account naming, and multi-entity handling vary by tenant). Text cells are sanitised against spreadsheet formula injection (`=`, `+`, `-`, `@` are neutralised).

## Configuration

Environment variables (or a local `.env`, see `.env.example`; real env vars win). Secrets are only ever read from the environment.

| Variable | Purpose | Default |
|---|---|---|
| `DEMO_MODE` | Seed the synthetic clients/mappings and offer the sample files (and the demo sign-in shortcuts). **Demo only.** | off |
| `SECRET_KEY` | Session signing key (32+ chars). If unset, a per-process key is used and everyone is signed out on restart | random per run |
| `APP_ENV` | `production` is **refused** while sign-in is self-declared | `demo` |
| `COOKIE_SECURE` | Mark session cookie HTTPS-only (set `true` on any HTTPS host; also turns on HSTS) | `false` |
| `ACCESS_CODE` | Optional shared code (8+ chars) required on the sign-in form. **Set it for any copy others can reach** | unset |
| `PORT` | Port to listen on when started via the Dockerfile (hosts set this) | `8000` |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL` | Enable real AI suggestions | unset → mock |
| `DATA_DIR` | Database, uploads, exports | `./data` |
| `MAX_UPLOAD_MB`, `MAX_ROWS`, `MAX_COLUMNS` | Upload limits | 5 / 20000 / 100 |
| `UPLOAD_RETENTION_DAYS` | Auto-delete uploads and exports after N days | 30 |
| `DELETE_AFTER_EXPORT_DEFAULT` | Pre-tick "delete source after export" | true |

The app **refuses to start** if `APP_ENV=production` (sign-in is not verified, so it is not allowed there) or if a `SECRET_KEY` is set but shorter than 32 characters.

## Sign-in today, and adding Okta later

**Today sign-in is self-declared.** The sign-in page asks for a **name**, an **email** and a **role** (Preparer, Reviewer or Admin). The app records them in the session and the audit log. **Nothing verifies them**: anyone can type any name, any email and any role, including Admin. What the form does give you:

* every action is attributed to a name and email in the audit log (logins are logged as `"verified": false`);
* the rules that depend on *who* did something still work, keyed on the email: nobody can approve a mapping or export they prepared themselves. That is only as strong as people's honesty, because someone could simply sign in with a different email;
* the role limits are still enforced on the server for every action.

Because it is not authentication, it is for the synthetic demo only: **`APP_ENV=production` is refused**, and a banner on every page says sign-in is self-declared. Don't put real client data behind it.

**To add Okta (or another identity provider) later**, everything downstream already keys off one session object created in `app/auth.py::login_user(email, name, roles, method)`. Add a route that authenticates the person (for Okta, an OIDC Authorization Code + PKCE flow, e.g. with Authlib, using the `groups` claim to decide roles with no matching group meaning no access), have it call `login_user` with the *verified* email and name, remove the self-declared form and its role choice, and lift the `APP_ENV=production` guard in `app/config.py`. Roles, segregation of duties and the audit trail need no changes. A previous revision of this repo contained a working Okta/Authlib implementation (commit `c660904`) that can be used as a starting point.

## Hosting a copy for others to open

The app is a normal container (`Dockerfile`) that listens on `$PORT` and answers `GET /healthz`, so any host that runs a Dockerfile can serve it. This section uses [Render](https://render.com) as the worked example because its setup is mostly clicking.

**What protects a hosted copy.** Sign-in is still self-declared (see above), so on its own anyone who finds the URL could sign in as Admin. Setting `ACCESS_CODE` adds one **shared code** to the sign-in form: people need the code *and* then type their own name, email and role. That is a shared password, not individual accounts: anyone you give the code to can choose any role, and you can't revoke one person. Wrong codes are throttled (10 per 5 minutes per address) and the attempted code is never logged or echoed. The site also asks search engines not to index it, sends HSTS over HTTPS, and `APP_ENV=production` stays refused. **Synthetic data only; don't upload real client data to a hosted copy.**

**What has and hasn't been tested.** Tested: the app, the access code and throttle, the health check, the security headers, and the container's exact start command run directly from a copy holding only the files the image copies. **Not tested:** building the Docker image (the dev sandbox has no Docker daemon) and deploying to Render (the sandbox couldn't reach render.com). `render.yaml` was written from memory. If something fails, the error will be loud and the manual settings below are equivalent.

### On Render

1. Create an account at render.com using **Sign in with GitHub**, and allow it to read `stephenmcnulty/helloworld`.
2. **New → Blueprint**, pick the repo and the branch `claude/focused-gates-wj776d` (or merge that branch into your default branch first and pick that).
3. When it asks for **`ACCESS_CODE`**, enter a code of 8+ characters. Render generates `SECRET_KEY` itself.
4. Apply. The first build takes a few minutes; the site appears at a `https://journal-entry-prep-….onrender.com` address.
5. Send people the address and the code. They enter the code, their name, email and a role.

If the Blueprint is rejected, use **New → Web Service** and set: runtime **Docker**; Dockerfile path `./jeprep/Dockerfile`; Docker build context directory `./jeprep`; health check path `/healthz`; and these environment variables:

| Variable | Value |
|---|---|
| `DEMO_MODE` | `true` |
| `APP_ENV` | `demo` |
| `COOKIE_SECURE` | `true` |
| `SECRET_KEY` | a random string of 32+ characters (`python -c "import secrets; print(secrets.token_urlsafe(48))"`) |
| `ACCESS_CODE` | the shared code, 8+ characters |

### Other hosts

Fly.io, Railway, Google Cloud Run and Azure Container Apps all run a Dockerfile and provide `$PORT`; use the same environment variables. The container trusts forwarded-address headers from whatever is in front of it (so throttling sees real client addresses), which is only safe because the host's HTTPS proxy is the sole way in: never publish the container's port directly to the internet.

### Running it

* **Idle and restarts.** Free tiers typically put the site to sleep when idle (the first visit afterwards is slow) and use a disk that is wiped on restart or redeploy. Here that means the seeded sample data comes back, but uploads, exports and the audit log are lost. Check your host's current terms; for a leadership demo, open the site a few minutes beforehand.
* **Changing the code.** Edit `ACCESS_CODE` and redeploy. People already signed in stay signed in until their session ends (8 hours); change `SECRET_KEY` as well to sign everyone out.
* **Updating the app.** Push to the deployed branch; the host rebuilds.
* **Local container.** `docker build -t journal-entry-prep jeprep && docker run -p 8000:8000 -e ACCESS_CODE=choose-a-code journal-entry-prep`, then <http://localhost:8000>.

## Security and governance built in

* **AuthZ** - self-declared sign-in (see above), deny-by-default roles enforced on every route; CSRF tokens on every POST; fresh session on login; open-redirect-safe `next`; secure/same-site cookies; CSP, `X-Frame-Options`, `nosniff`, `no-store`.
* **Audit log** (`app/audit.py`) - append-only (DB triggers reject UPDATE/DELETE) and **hash-chained**, so edits are detectable; the Admin page verifies the chain. Records who, when, action, client, job, **mapping version used**, **SHA-256 of the uploaded file**, **who approved the export**, plus refused attempts (e.g. self-approval) and AI-suggestion calls (whether anything was sent externally).
* **Uploads** - `.csv`/`.xlsx` only; size, row and column limits; magic-byte and content checks; macro workbooks and zip bombs rejected; XML hardened via `defusedxml`; stored under a random name with `0600` permissions in a `0700` folder, never served statically; formulas are never evaluated.
* **Retention** - uploads and exports are purged after `UPLOAD_RETENTION_DAYS` (at startup and on demand); a per-job **delete after export** option removes the source report immediately; deletions are audited.
* **No secrets in code or repo** - `.env`, `data/` are git-ignored; `.env.example` has blanks.

## Project layout

```
app/
  main.py config.py db.py        app factory, env settings, SQLite schema
  auth.py audit.py               self-declared sign-in, roles, CSRF; hash-chained audit log
  storage.py                     upload validation, private storage, retention
  healthcheck.py                 container health probe (Dockerfile HEALTHCHECK)
  parsing.py money.py            CSV/XLSX -> report (Decimal only); layout signature
  domain.py rules.py mapping.py  client config + mapping lines; header rules; versioned mappings
  redaction.py suggest.py        PII tokenizer; suggest_mapping() (Claude or labelled mock)
  allocation.py journal.py       percentage splits + due-to/from; draft journal builder
  validation.py exporters.py     the five checks; Intacct and QBO CSV writers
  workflow.py                    job state machine, segregation of duties, audit calls
  web/                           FastAPI routers (wizard, review, admin, login); templates/ static/
  demo/                          synthetic data generator and DB seed
demo_data/                       generated sample registers (synthetic)
artifact/                        single-file browser walkthrough: template, build script, engine-parity check
Dockerfile .dockerignore         container image (see "Hosting a copy"); ../render.yaml is a Render Blueprint
tests/                           pytest suite
```

## Browser walkthrough (no server needed)

`artifact/` builds a single self-contained HTML page that walks through the same flow in the browser, for people who can't run the Python app. It is a **JavaScript re-implementation of the engine** (rules, mock suggestion, allocation, the five checks, Intacct/QBO export, hash-chained audit log), seeded from the same synthetic data. It has no server, no real sign-in, no live Claude call and no file downloads (it offers *Copy CSV* instead).

```bash
python artifact/build.py --out /tmp/page.html --expected /tmp/expected.json
node artifact/verify_engine.js /tmp/page.html /tmp/expected.json   # 125 comparisons vs the Python engine
```

`verify_engine.js` replays nine cases through the JS engine and compares them with the Python engine's output: mapping lines, journal lines, every check's status and message, tie-out rows, the redacted sample rows, and the exported CSV byte for byte. Re-run it after changing either engine.

## What is real, what is mocked

| Area | Status |
|---|---|
| Parsing, rules, allocation math, validation checks, journal builder, exports, audit chain, roles/SoD, upload hardening, retention | **Real and tested** |
| Wizard UI and the whole flow end to end (driven through a real browser during development) | **Real** |
| Sign-in | **Self-declared name/email/role - not verified.** Okta was removed for now and can be added later |
| `suggest_mapping()` with `ANTHROPIC_API_KEY` | **Implemented; the request shape was verified against the installed SDK through a mock HTTP transport, but not against the live API** (no key was available). Output quality on real layouts is unknown until tried. |
| `suggest_mapping()` without a key | **Mock** keyword heuristic, labelled "MOCK SUGGESTION" in the UI, audit log and notices |
| Intacct / QBO CSV column layouts | **Best-effort reconstruction - verify against the client's tenant** |
| Chart of accounts, entities, funds, clients | **Synthetic** seed data |
| Posting to Intacct/QBO | **Deliberately absent** |

## What would be needed for production

1. **Real sign-in** (Okta or similar: app registration, group provisioning - see *Adding Okta later* above), HTTPS termination, `COOKIE_SECURE`, a real `SECRET_KEY` from a secret manager, session idle timeout and RP-initiated logout (single logout isn't implemented).
2. **Real import templates** - download each client's current Intacct (and tenant dimension names for entity/fund) and QBO import templates; confirm journal symbol, dimensions, account naming/numbers, date format, multi-entity behaviour; add per-client export profiles and golden-file tests; do a trial import in a sandbox company.
3. **Real mappings and charts** - import each client's chart of accounts, entities and funds from their system instead of seed data; per-client entitlements (who may see which client).
4. **More report types and layouts** - only the wide-format *Payroll Register* exists (one row per employee, one column per pay element); long-format registers, multi-sheet workbooks, state/local taxes, accruals and reversing entries are not handled.
5. **IT / security review** - threat model, pen test, dependency scanning, logging/monitoring and alerting, backup/restore, data-residency and retention policy sign-off, and a vendor/data-processing review for sending *redacted* payroll structure to the Anthropic API (confirm that is acceptable, consider zero-retention terms, and decide whether amounts should also be generalised).
6. **Hardening** - replace SQLite with a managed database if concurrency grows; encrypt files at rest (or use an encrypted volume); virus-scan uploads; ship the audit log to an external write-once store (the in-DB hash chain is tamper-*evident*, not tamper-*proof* against a DBA); rate-limit; move retention to a scheduled job.
7. **Validation of AI suggestions at scale** - an evaluation set of real (de-identified) layouts, monitoring of how often reviewers change suggestions, and handling of model refusals/outages (currently falls back to the labelled mock).

## Known limitations

* One sheet (the first) of a workbook is read; Excel formulas are read as cached values.
* The journal posts one line per mapped column (plus offset/allocation lines); there is no per-department/class breakdown.
* A single `pay_date` column is checked against the pay period; registers where pay dates legitimately fall after the period end would need a different date rule.
* The wizard is resumable but not collaborative: two people editing the same draft mapping at once is last-write-wins.
