import Ask from "./ask";

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-8 px-4 py-12">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">BizWiz</h1>
        <p className="mt-1 text-stone-600">
          Ask a question about Ironbark Line Freight&apos;s documents. Every answer shows where it
          came from.
        </p>
      </header>
      <Ask />
    </main>
  );
}
