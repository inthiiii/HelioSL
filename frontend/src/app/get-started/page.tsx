import Link from "next/link";

import { HelioLogo } from "@/components/brand/helio-logo";


const steps = [
  {
    number: "01",
    title: "Build your energy picture",
    description: "Bring your electricity use, bills and rooftop-solar records into one private view.",
  },
  {
    number: "02",
    title: "Understand what is changing",
    description: "See trends, possible anomalies and plain-language insights without jumping to unsupported conclusions.",
  },
  {
    number: "03",
    title: "Make better everyday decisions",
    description: "Explore solar scenarios and ask HelioSL questions with visible sources, agents and safety checks.",
  },
];


export default function GetStartedPage() {
  return (
    <main className="min-h-screen overflow-hidden bg-[#06110d] text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_20%,rgba(52,211,153,0.17),transparent_31%),radial-gradient(circle_at_85%_82%,rgba(250,204,21,0.09),transparent_30%)]" />
      <header className="relative z-10 mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
        <HelioLogo />
        <Link href="/" className="text-sm text-white/55 transition hover:text-white">
          Back to home
        </Link>
      </header>

      <section className="relative z-10 mx-auto max-w-6xl px-6 pb-20 pt-12 lg:px-8 lg:pt-20">
        <div className="mx-auto max-w-3xl text-center">
          <span className="inline-flex rounded-full border border-emerald-400/25 bg-emerald-400/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-emerald-200">
            Before you begin
          </span>
          <h1 className="mt-7 text-4xl font-semibold tracking-[-0.045em] sm:text-6xl">
            A clearer energy day starts with understanding your own data.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-white/58">
            HelioSL is designed to help Sri Lankan households and businesses
            notice changes earlier, plan with clearer assumptions and make
            renewable-energy choices with more confidence.
          </p>
        </div>

        <div className="mt-14 grid gap-4 md:grid-cols-3">
          {steps.map((step) => (
            <article key={step.number} className="rounded-[1.75rem] border border-white/10 bg-white/[0.045] p-7 backdrop-blur">
              <span className="font-mono text-xs text-emerald-300">{step.number}</span>
              <h2 className="mt-7 text-xl font-semibold">{step.title}</h2>
              <p className="mt-3 text-sm leading-6 text-white/50">{step.description}</p>
            </article>
          ))}
        </div>

        <div className="mx-auto mt-10 max-w-3xl rounded-[1.75rem] border border-emerald-400/20 bg-emerald-400/[0.07] p-7 sm:flex sm:items-center sm:justify-between sm:gap-8">
          <div>
            <h2 className="text-lg font-semibold">What you get from day one</h2>
            <p className="mt-2 text-sm leading-6 text-white/52">
              A personal dashboard, energy and solar tracking, scenario planning,
              bill import and an accountable AI assistant. You stay in control of
              the information you add.
            </p>
          </div>
          <Link
            href="/register"
            className="mt-6 inline-flex shrink-0 items-center justify-center rounded-xl bg-emerald-400 px-6 py-3.5 font-semibold text-[#06110d] transition hover:bg-emerald-300 sm:mt-0"
          >
            Create my account →
          </Link>
        </div>

        <p className="mt-7 text-center text-sm text-white/38">
          Already a member?{" "}
          <Link href="/login" className="font-medium text-emerald-300 hover:text-emerald-200">
            Sign in to your dashboard
          </Link>
        </p>
      </section>
    </main>
  );
}
