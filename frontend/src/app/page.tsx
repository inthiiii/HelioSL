import Link from "next/link";


export default function HomePage() {
  return (
    <main className="min-h-screen bg-neutral-950 px-6 py-20 text-white">
      <div className="mx-auto max-w-5xl">
        <p className="text-sm text-emerald-400">
          HelioSL
        </p>

        <h1 className="mt-5 max-w-3xl text-5xl font-semibold leading-tight">
          Smarter renewable energy decisions for Sri Lanka.
        </h1>

        <p className="mt-6 max-w-2xl text-lg text-neutral-400">
          An Agentic AI platform for solar energy intelligence,
          performance analysis, trusted renewable-energy knowledge,
          and personalized decision support.
        </p>

        <div className="mt-10 flex gap-4">
          <Link
            href="/register"
            className="rounded-lg bg-emerald-500 px-5 py-3 font-medium text-black"
          >
            Get started
          </Link>

          <Link
            href="/login"
            className="rounded-lg border border-neutral-700 px-5 py-3 text-neutral-200"
          >
            Sign in
          </Link>
        </div>
      </div>
    </main>
  );
}