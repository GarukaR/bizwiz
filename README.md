# BizWiz

Ask questions of your business data and get quick, accurate answers, each with citations that show exactly
where the answer came from.

🚧 **In progress. v1 target: end of January 2027.** See [`PLAN.md`](PLAN.md) for the design and
[`docs/STATE.md`](docs/STATE.md) for progress.

The public demo runs on **Ironbark Line Freight**, a fictional Melbourne freight company. Any resemblance to
a real business is unintended.

## Run it locally

You need Docker Desktop (running), [uv](https://docs.astral.sh/uv/) and Node 24. Then, from the repo
root in PowerShell:

```
.un.ps1
```

It starts the database, the API and the web app, and opens http://localhost:3010. Press Ctrl+C to
stop. On the first run it creates `.env` from `.env.example`. With no `ANTHROPIC_API_KEY` in `.env` it
uses the fake answerer (it quotes the best-matching document), so it works before you have a key.

To run the pieces one at a time instead:

| What | Command (from the repo root) |
|---|---|
| Start the database | `docker compose up -d db` |
| Start the API (port 8010) | `cd backend && uv run bizwiz-api` |
| Start the web app (port 3010) | `cd frontend && npm install && npm run dev -- --port 3010` |
| Run the backend tests | `cd backend && uv run pytest` |
| Run the end-to-end test | `cd frontend && npm run e2e` |
| Smoke-test the real Claude API | `cd backend && uv run python scripts/smoke.py "What is the fuel levy?"` |

The API indexes `corpus/ironbark/` when it starts. The end-to-end test starts its own API and web app
on ports 8011 and 3011 with a fake answerer, so it never calls the paid API.
