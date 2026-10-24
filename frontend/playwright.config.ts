import { defineConfig } from "@playwright/test";

// The e2e run starts its own API and web app on their own ports, with the fake answerer,
// so it never calls the paid Claude API. Postgres must be up: `docker compose up -d db`.
const API_PORT = 8011;
const WEB_PORT = 3011;

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  use: { baseURL: `http://localhost:${WEB_PORT}` },
  webServer: [
    {
      command: "uv run bizwiz-api",
      cwd: "../backend",
      url: `http://localhost:${API_PORT}/docs`,
      env: {
        ANSWERER: "fake",
        API_PORT: String(API_PORT),
        WEB_ORIGIN: `http://localhost:${WEB_PORT}`,
      },
      timeout: 60_000,
    },
    {
      command: `npm run dev -- --port ${WEB_PORT}`,
      url: `http://localhost:${WEB_PORT}`,
      env: { NEXT_PUBLIC_API_URL: `http://localhost:${API_PORT}` },
      timeout: 120_000,
    },
  ],
});
