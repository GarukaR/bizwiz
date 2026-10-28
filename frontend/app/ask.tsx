"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8010";

type Citation = {
  passage_id: string;
  quoted_text: string;
  doc_title: string;
  location: string;
};

type AskResponse = { answer: string; citations: Citation[] };

type Passage = { id: string; doc_title: string; text: string; location: string };

export default function Ask() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<AskResponse | null>(null);
  const [open, setOpen] = useState<{ passage: Passage; quote: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function onAsk(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setBusy(true);
    setError("");
    setResult(null);
    setOpen(null);
    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error(`The server said ${res.status}`);
      setResult(await res.json());
    } catch (err) {
      setError(`Couldn't get an answer. ${(err as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  async function openCitation(c: Citation) {
    setError("");
    try {
      const res = await fetch(`${API_URL}/passages/${encodeURIComponent(c.passage_id)}`);
      if (!res.ok) throw new Error(`The server said ${res.status}`);
      setOpen({ passage: await res.json(), quote: c.quoted_text });
    } catch (err) {
      setError(`Couldn't open that source. ${(err as Error).message}`);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <form onSubmit={onAsk} className="flex flex-col gap-2 sm:flex-row">
        <label htmlFor="question" className="sr-only">
          Your question
        </label>
        <input
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What is the fuel levy?"
          className="flex-1 rounded-md border border-stone-300 bg-white px-3 py-2 text-stone-900 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-600/20"
        />
        <button
          type="submit"
          disabled={busy}
          className="rounded-md bg-teal-700 px-4 py-2 font-medium text-white hover:bg-teal-800 disabled:opacity-60"
        >
          {busy ? "Thinking…" : "Ask"}
        </button>
      </form>

      {error && (
        <p role="alert" className="text-red-700">
          {error}
        </p>
      )}

      {result && (
        <section aria-label="Answer" className="flex flex-col gap-3">
          <p data-testid="answer" className="whitespace-pre-wrap leading-relaxed">
            {result.answer}
          </p>
          {result.citations.length > 0 && (
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-sm text-stone-500">Sources:</span>
              {result.citations.map((c, i) => (
                <button
                  key={i}
                  type="button"
                  data-testid="citation"
                  onClick={() => openCitation(c)}
                  title={c.quoted_text}
                  className="rounded-full border border-teal-700/30 bg-teal-50 px-3 py-1 text-sm text-teal-900 hover:bg-teal-100"
                >
                  [{i + 1}] {c.doc_title}
                </button>
              ))}
            </div>
          )}
        </section>
      )}

      {open && (
        <aside
          data-testid="passage"
          aria-label="Source passage"
          className="rounded-md border border-stone-200 bg-stone-50 p-4"
        >
          <div className="mb-2 flex items-baseline justify-between gap-4">
            <h2 className="font-semibold">{open.passage.doc_title}</h2>
            <button
              type="button"
              onClick={() => setOpen(null)}
              className="text-sm text-stone-500 hover:text-stone-800"
            >
              Close
            </button>
          </div>
          <p className="mb-3 text-xs uppercase tracking-wide text-stone-500">
            {open.passage.location}
          </p>
          <Highlighted text={open.passage.text} quote={open.quote} />
        </aside>
      )}
    </div>
  );
}

function Highlighted({ text, quote }: { text: string; quote: string }) {
  const at = quote ? text.indexOf(quote) : -1;
  if (at < 0) return <pre className="whitespace-pre-wrap font-sans text-sm">{text}</pre>;
  return (
    <pre className="whitespace-pre-wrap font-sans text-sm">
      {text.slice(0, at)}
      <mark className="rounded bg-amber-200 px-0.5">{quote}</mark>
      {text.slice(at + quote.length)}
    </pre>
  );
}
