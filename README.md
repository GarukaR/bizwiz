# BizWiz

Ask questions of your business data and get quick, accurate answers, each with citations that show exactly
where the answer came from.

🚧 **In progress. v1 target: end of January 2027.** See [`PLAN.md`](PLAN.md) for the design and
[`docs/STATE.md`](docs/STATE.md) for progress.

The public demo runs on **Ironbark Line Freight**, a fictional Melbourne freight company. Any resemblance to
a real business is unintended.

## Run it locally

You need Docker, [uv](https://docs.astral.sh/uv/) and Node 24. Copy `.env.example` to `.env` first.
Set `ANSWERER=fake` there to try it without an Anthropic API key.

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
