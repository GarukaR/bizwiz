# BizWiz plan

Decisions from the planning session on 2026-10-25. Treat them as settled unless Garuka reopens one.
Progress lives in `docs/STATE.md`, not here.

## What BizWiz is

Ask questions of your business data and get quick, accurate answers, each with citations that show
exactly where the answer came from.

It finishes a transport-industry project Garuka didn't deliver, so it has two jobs:

1. **Portfolio piece**: public repo, live demo, and an eval report with real numbers.
2. **Real tool**: True Theorem (Garuka's consultancy) uses it on its own Google Drive. Built so other
   businesses could use it later.

## Decisions

### 1. Done = shipped and measured

A finished, measured thing beats a bigger unfinished one. The eval report is the proof.

### 2. Build order

1. **Q&A over documents** (Google Drive docs, PDFs, Word files). Classic RAG. **= v1**
2. **Weekly insights digest**: questions BizWiz runs on a schedule over your own data, every line cited.
3. **Research mode**: web research written up as a cited, dated report. A human reviews it before it is
   saved and indexed.
4. **Numbers**: Sheets and Postgres through text-to-SQL, plus charts.
5. **Mongo**, plus a router that picks the engine for each question or combines them.

### 3. Test questions are real questions

Every answer type gets golden questions: lookup, synthesis, numbers, freshness (the newest document
wins), not in the documents (must say "couldn't find it"), and business-growth questions (best clients,
win/loss reasons, revenue concentration).

Starter questions for True Theorem's private eval. The answers belong only in `evals/private/`. Client
names are left generic here.

- **Lookup:** What payment milestones do we use? What's the starting price of the Dashboard package? What's in
  the care plan and what does it cost? What did we propose to client X? What stack did we use for client X?
- **Synthesis:** What do we promise about reply times across all documents? Which past projects involved IoT
  or data pipelines? What risks did we flag in proposals? Summarise everything we know about client X.
- **Numbers (Phase 4):** How much have we invoiced this financial year? Which invoices are unpaid? Total
  quoted this year?
- **Freshness:** What's our *current* founding-client discount? What's the latest version of our terms of
  engagement, and what changed?
- **Not in the documents:** What's our ABN (if no document has it)? What did client X pay in total? Who's our
  accountant?
- **Process:** Steps from a new lead to a signed project? What did the Zoho report recommend? Our standard
  reply when a lead wants a call straight away?
- **Growth:** Which service earns the most per hour? What do our best clients have in common? Why did we lose
  the proposals we lost? What share of revenue comes from our biggest client? Which past clients haven't
  heard from us in 3 months?

### 4. Knowledge boundary

- BizWiz answers **only from your own data**. That is what makes "grounded" testable.
- External research comes in only as **reviewed, dated documents**.
- Advice is allowed but always split into **"From your records:"** (cited) and **"Suggestion:"**
  (opinion).

### 5. Visual answers

- Phase 1: **cited comparison tables**, and a **source preview** that opens with the cited passage
  highlighted.
- Phase 2: **charts** from a fixed set (bar, line, number tile, table) written as Vega-Lite specs.
  **The model never writes chart numbers.** It picks the chart's shape, our code fills in the real rows,
  and each chart cites the rows and query it was built from.
- Not planned yet: reading images or scanned pages inside documents.

### 6. Vertical slices

Every issue cuts through the whole stack and ends with something you can click. The eval score has its
own page in the app. Deployed early, kept deployed.

### 7. Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.12, FastAPI, `uv`, `ruff` |
| Store + search | Postgres + pgvector on Neon: vector search and full-text search in one database, plus app data |
| Embeddings | Voyage AI (`model_id` stored with every vector) |
| Models | Claude Haiku 5.5 / Opus 5.5 / Sonnet 5.5 (see 9) |
| Citations | Claude API built-in citations (`citations: {enabled: true}` on document blocks) |
| Parsing | Google Drive API exports, `python-docx`, `pypdf` (not PyMuPDF, which is AGPL) |
| Frontend | Next.js + Tailwind; Vega-Lite charts from Phase 2 |
| Tests | `pytest` with fakes · integration tests on real Postgres + pgvector · Playwright end-to-end test per slice · eval suite with real models |

The RAG core is **hand-written**, with no LangChain or LlamaIndex: it's the part being learned, and
hand-written code is easier to test. Libraries handle parsing and the Google APIs.

### 8. Four seams, at the domain level

```python
class Source(Protocol):    # list_changed(since), load(ref) -> Document  (local folder, Drive, later DBs)
class Embedder(Protocol):  # model_id; embed(texts) -> vectors
class Index(Protocol):     # add(chunks); search(query, k, filters) -> passages  (hybrid inside)
class Answerer(Protocol):  # answer(question, passages) -> Answer(text, citations)
```

- The seams describe what BizWiz needs, not a generic `complete(prompt)` wrapper. That keeps each
  provider's best features usable (Claude's native citations).
- One real implementation per seam, plus fakes for tests. No speculative adapters, no DI framework.
- The `ask()` pipeline imports only the seams. Concrete classes are wired up in one place.
- A reranker becomes a fifth seam later, only if the eval shows retrieval is the weak point.

### 9. Models per pipeline step

| Step | Model |
|---|---|
| Chunk context line at index time (Anthropic's *Contextual Retrieval*) | Haiku 5.5 + prompt caching |
| Query rewriting / question type | Haiku 5.5 |
| Answer + citations | Opus 5.5; Sonnet 5.5 measured against it on the eval |
| Eval judge | Opus 5.5, fixed version, checked against Garuka's hand grades |

Every step reads its model from config. No routing between models until the eval and the bill show a
reason. Rough cost is about 3 US cents per question on Opus.

### 10. Access and safety

- Reads **one `BizWiz` Drive folder** at first (True Theorem account), then an **allow-list** of folders.
  Never the whole Drive.
- Secret filter: anything that looks like passwords, API keys or card numbers is skipped and the skip is
  logged.
- Drive scopes: **read-only** for sources; **`drive.file`** (only files BizWiz created) for "Export to
  Google Doc".
- Sign-in: Google sign-in with an email allow-list (Garuka and their brother). No sign-up page.
- Every chunk records who could see its source document. Enforced later, when a business with staff
  uses BizWiz; the filter then runs *before* retrieval.
- Contact details: can answer about one contact, but never exports or bulk-lists them (Australian
  Privacy Act; also limits damage from prompt injection).
- Treat retrieved text as data, never instructions (indirect prompt injection).

### 11. Outputs

- Answers, digests and reports are stored in BizWiz's own Postgres, with **data snapshots** so old
  reports can be reproduced.
- BizWiz **never indexes its own output.** The one exception is research reports a human approved,
  which come in as a separate, clearly labelled "Approved research" source.

### 12. Public and private

| | Public | Private |
|---|---|---|
| Code | `GarukaR/bizwiz` (public) | same code |
| Corpus | **Ironbark Line Freight**, a fictional Melbourne freight company: contracts, rate cards, SLAs, incident reports, driver handbook (Chain of Responsibility, fatigue), maintenance notes, quotes, marketing plan, with deliberate traps | True Theorem's `BizWiz` Drive folder |
| Eval | In the repo; the README shows the score | Kept out of git |
| App | Public demo with a daily spending cap | Sign-in limited to the two founders |

In Phase 2 the demo company also gets Postgres tables (trips, deliveries, vehicles, fuel, invoices).
Phase 3 adds Mongo (telematics events, support tickets).

### 13. Hosting

Backend on Render (Singapore) · Neon in the same region · frontend on Cloudflare Workers · scheduled jobs
(Drive sync, digest) through GitHub Actions calling a protected endpoint · daily spending cap on the
demo. Render's free tier sleeps; the always-on plan is about US$7/month if True Theorem needs it.

### 14. v1 definition of done (target: **end of January 2027**)

Quality bar, on the demo corpus eval:

| Metric | Bar |
|---|---|
| Correct answers (answerable questions) | ≥ 85% |
| "Couldn't find it" on unanswerable questions | 100% |
| Citation validity: quote exists in source *and* supports the claim | 100% |
| Freshness traps | all pass |
| Speed (server awake) | first words ≤ 3 s, full answer ≤ 15 s |
| Cost per question | reported |

Shipped means all four:

1. Public repo with a README: architecture diagram, how to run it, and the eval report with misses
   included.
2. Live public demo.
3. True Theorem uses it for real for 2 weeks; anything it gets wrong is added to the private eval.
4. A write-up: what was built, what was measured, what was learned.

Not in v1: follow-up questions or conversation memory, the digest, research mode, Sheets and charts.

### 15. Who writes what: Quest Mode

- **Garuka writes the RAG core** through Quest Mode (`docs/quests/README.md`): 30-minute stages, test-first.
- **Claude** writes the tests for each quest, plus all the plumbing (Drive, auth, routes, UI, deploy, demo
  corpus). Every plumbing PR includes a short "what and why" note.
- **Garuka owns the eval**: golden questions, hand-grading samples, reading the eval page.

## Expert input behind these decisions

- **Positioning** (David C. Baker, *The Business of Expertise*): expertise grows out of past work, and
  positioning means choosing one focus. This is where the "best clients / best margins" questions come
  from.
- **Consultancy metrics**: win rate, client concentration (keep any one client under about 15–20% of
  revenue), repeat revenue, margin per project, lifetime value vs cost to win a client. Most of these need
  records True Theorem doesn't keep yet. Phase 4 will suggest a Leads / Projects / Invoices sheet.
- **Enterprise RAG practice**: filter permissions before retrieval, hybrid search (vectors confuse exact
  terms like years and names), freshness, citations with previews, continuous evaluation.
- **Security**: indirect prompt injection through indexed content. Defences come in layers: control what
  goes into the corpus, keep tools least-privilege, and add no outbound actions without review.
