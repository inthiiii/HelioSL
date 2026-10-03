import Image from "next/image";
import Link from "next/link";

import { SolarPathFinder } from "@/components/landing/solar-path-finder";


const features = [
  {
    number: "01",
    title: "Energy intelligence",
    description: (
      "Turn monthly electricity records into clear trends, " +
      "comparisons and responsible next steps."
    ),
  },
  {
    number: "02",
    title: "Solar performance",
    description: (
      "Compare generation history with live environmental context " +
      "without presenting correlation as confirmed causation."
    ),
  },
  {
    number: "03",
    title: "Trusted Sri Lankan knowledge",
    description: (
      "Retrieve guarded evidence from recognized regulators, " +
      "utilities and public energy authorities."
    ),
  },
  {
    number: "04",
    title: "Scenario planning",
    description: (
      "Explore capacity, generation, coverage and payback using " +
      "explicit assumptions you can inspect and change."
    ),
  },
  {
    number: "05",
    title: "Agentic assistance",
    description: (
      "See Energy, Weather, Knowledge, Financial and Safety agents " +
      "cooperate live on every complex question."
    ),
  },
  {
    number: "06",
    title: "Privacy by design",
    description: (
      "Authenticated /me endpoints keep household and business " +
      "records scoped to the signed-in user."
    ),
  },
];


export default function HomePage() {
  return (
    <main className="overflow-hidden bg-[#06110d] text-white">
      <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-[#06110d]/85 backdrop-blur-xl">
        <nav className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
          <Link
            href="#home"
            className="flex items-center gap-3"
            aria-label="HelioSL home"
          >
            <span className="grid h-10 w-10 place-items-center rounded-xl bg-emerald-400 text-lg font-black text-[#06110d]">
              H
            </span>
            <span>
              <span className="block text-lg font-semibold tracking-tight">
                HelioSL
              </span>
              <span className="block text-[10px] uppercase tracking-[0.24em] text-emerald-300/80">
                Energy intelligence
              </span>
            </span>
          </Link>

          <div className="hidden items-center gap-8 text-sm text-white/65 md:flex">
            <Link className="transition hover:text-white" href="#why">
              Why HelioSL
            </Link>
            <Link className="transition hover:text-white" href="#solar-path">
              Find my path
            </Link>
            <Link className="transition hover:text-white" href="#platform">
              Platform
            </Link>
            <Link className="transition hover:text-white" href="#responsible-ai">
              Responsible AI
            </Link>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="hidden rounded-xl px-4 py-2 text-sm font-medium text-white/75 transition hover:text-white sm:block"
            >
              Log in
            </Link>
            <Link
              href="/register"
              className="rounded-xl bg-emerald-400 px-4 py-2.5 text-sm font-semibold text-[#06110d] transition hover:bg-emerald-300"
            >
              Get started
            </Link>
          </div>
        </nav>
      </header>


      <section
        id="home"
        className="relative isolate flex min-h-[92vh] items-center pt-28"
      >
        <div className="absolute inset-0 -z-20 bg-[radial-gradient(circle_at_18%_25%,rgba(52,211,153,0.18),transparent_32%),radial-gradient(circle_at_82%_70%,rgba(250,204,21,0.10),transparent_34%)]" />
        <div className="absolute inset-x-0 bottom-0 -z-10 h-40 bg-gradient-to-t from-[#06110d] to-transparent" />

        <div className="mx-auto grid w-full max-w-7xl items-center gap-14 px-6 py-20 lg:grid-cols-[1.05fr_0.95fr] lg:px-8">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/25 bg-emerald-400/10 px-4 py-2 text-xs font-medium uppercase tracking-[0.18em] text-emerald-200">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              Built for Sri Lankan energy decisions
            </div>

            <h1 className="mt-8 max-w-4xl text-5xl font-semibold leading-[1.04] tracking-[-0.045em] sm:text-6xl lg:text-7xl">
              See your energy.
              <span className="block text-emerald-300">
                Decide with evidence.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-lg leading-8 text-white/62">
              HelioSL brings consumption, rooftop-solar performance,
              live weather, trusted local knowledge and transparent AI
              agents into one accountable decision-support platform.
            </p>

            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href="/register"
                className="rounded-2xl bg-emerald-400 px-6 py-3.5 font-semibold text-[#06110d] shadow-[0_18px_60px_rgba(52,211,153,0.22)] transition hover:-translate-y-0.5 hover:bg-emerald-300"
              >
                Start with HelioSL
              </Link>
              <Link
                href="/login"
                className="rounded-2xl border border-white/15 bg-white/5 px-6 py-3.5 font-medium text-white transition hover:border-white/30 hover:bg-white/10"
              >
                Open your dashboard
              </Link>
            </div>

            <div className="mt-12 flex flex-wrap gap-x-8 gap-y-3 text-sm text-white/45">
              <span>✓ User-scoped private data</span>
              <span>✓ Trusted-source retrieval</span>
              <span>✓ Visible safety verification</span>
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-xl lg:mx-0 lg:ml-auto">
            <div className="absolute -inset-6 rounded-[2.5rem] bg-gradient-to-br from-emerald-400/20 to-yellow-300/5 blur-2xl" />
            <div className="relative overflow-hidden rounded-[2rem] border border-white/15 bg-white/5 p-3 shadow-2xl shadow-black/40">
              <div className="relative aspect-[4/5] overflow-hidden rounded-[1.45rem]">
                <Image
                  src="https://www.solanra.com/example/gallery/18-pelawatta-5kw-project.jpg"
                  alt="Rooftop solar installation on a Sri Lankan home"
                  fill
                  unoptimized
                  priority
                  sizes="(max-width: 1024px) 90vw, 42vw"
                  className="object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/5 to-transparent" />

                <div className="absolute inset-x-5 bottom-5 rounded-2xl border border-white/15 bg-black/55 p-5 backdrop-blur-xl">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-xs uppercase tracking-[0.18em] text-emerald-300">
                        Integrated intelligence
                      </p>
                      <p className="mt-2 text-xl font-semibold">
                        From raw records to responsible action
                      </p>
                    </div>
                    <div className="grid h-12 w-12 shrink-0 place-items-center rounded-full bg-emerald-400 font-bold text-[#06110d]">
                      AI
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>


      <section className="border-y border-white/10 bg-white/[0.025]">
        <div className="mx-auto grid max-w-7xl divide-y divide-white/10 px-6 sm:grid-cols-3 sm:divide-x sm:divide-y-0 lg:px-8">
          <Stat value="129,300+" label="rooftop connections by Sep 2025" />
          <Stat value="2,090 MW" label="reported rooftop capacity" />
          <Stat value="10%" label="of Q2 2025 generation from rooftop solar" />
        </div>
        <p className="pb-4 text-center text-[11px] text-white/35">
          Source: PUCSL, Analysis on Rooftop Solar Integration & Industry Growth, 2026.
        </p>
      </section>


      <SolarPathFinder />


      <section id="why" className="mx-auto max-w-7xl px-6 py-28 lg:px-8">
        <div className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.22em] text-emerald-300">
              Why Sri Lanka needs this
            </p>
            <h2 className="mt-5 text-4xl font-semibold tracking-[-0.035em] sm:text-5xl">
              Solar adoption is growing. Decision clarity must grow with it.
            </h2>
            <p className="mt-6 text-lg leading-8 text-white/58">
              Households and businesses need more than a bill calculator.
              They need their own records, credible public knowledge,
              environmental context and visible uncertainty brought together
              before making technical or financial decisions.
            </p>

            <div className="mt-8 space-y-4">
              {[
                "Fragmented energy, solar and policy information",
                "Performance changes that require evidence—not guesses",
                "Financial decisions that depend on explicit assumptions",
              ].map((item) => (
                <div className="flex gap-3 text-white/75" key={item}>
                  <span className="mt-1 grid h-5 w-5 shrink-0 place-items-center rounded-full bg-emerald-400/15 text-xs text-emerald-300">
                    ✓
                  </span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <PhotoCard
              src="https://macksonssolar.com/wp-content/uploads/2024/07/puttalam.jpeg"
              alt="Sri Lankan rooftop solar panels in a tropical setting"
              eyebrow="Households"
              title="Understand usage and rooftop performance together"
              className="sm:translate-y-8"
            />
            <PhotoCard
              src="https://www.dimolanka.com/wp-content/uploads/2025/09/Renewable-Energy-Expansion-1435x445-1.jpg"
              alt="Commercial renewable-energy installation"
              eyebrow="Businesses"
              title="Plan around larger loads and commercial realities"
            />
          </div>
        </div>
      </section>


      <section id="platform" className="border-y border-white/10 bg-[#091712] py-28">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="max-w-3xl">
            <p className="text-sm font-medium uppercase tracking-[0.22em] text-emerald-300">
              One connected platform
            </p>
            <h2 className="mt-5 text-4xl font-semibold tracking-[-0.035em] sm:text-5xl">
              Intelligence you can inspect, not just an answer you must trust.
            </h2>
          </div>

          <div className="mt-14 grid gap-px overflow-hidden rounded-[2rem] border border-white/10 bg-white/10 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <article className="bg-[#091712] p-8" key={feature.number}>
                <p className="font-mono text-xs text-emerald-300/70">
                  {feature.number}
                </p>
                <h3 className="mt-8 text-xl font-semibold">
                  {feature.title}
                </h3>
                <p className="mt-4 leading-7 text-white/52">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>


      <section className="mx-auto max-w-7xl px-6 py-28 lg:px-8">
        <div className="rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/[0.07] to-transparent p-8 sm:p-12">
          <div className="grid gap-12 lg:grid-cols-[0.75fr_1.25fr] lg:items-center">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.22em] text-yellow-200">
                Visible agent cooperation
              </p>
              <h2 className="mt-5 text-4xl font-semibold tracking-[-0.035em]">
                Every specialist has a job. Every step leaves a trace.
              </h2>
              <p className="mt-5 leading-7 text-white/55">
                HelioSL makes orchestration visible while it analyses your
                question, retrieves evidence, checks planning inputs and
                verifies the final response.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              {[
                ["01", "Understand the question"],
                ["02", "Select specialist agents"],
                ["03", "Analyse records and context"],
                ["04", "Retrieve guarded evidence"],
                ["05", "Synthesize a clear response"],
                ["06", "Run safety verification"],
              ].map(([number, label]) => (
                <div
                  className="flex items-center gap-4 rounded-2xl border border-white/10 bg-black/20 p-4"
                  key={number}
                >
                  <span className="font-mono text-xs text-emerald-300">
                    {number}
                  </span>
                  <span className="text-sm text-white/75">
                    {label}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>


      <section id="responsible-ai" className="mx-auto max-w-7xl px-6 pb-28 lg:px-8">
        <div className="grid overflow-hidden rounded-[2rem] border border-emerald-400/20 bg-emerald-400/[0.07] lg:grid-cols-2">
          <div className="p-9 sm:p-14">
            <p className="text-sm font-medium uppercase tracking-[0.22em] text-emerald-300">
              Responsible by design
            </p>
            <h2 className="mt-5 text-4xl font-semibold tracking-[-0.035em]">
              Clear about evidence. Honest about uncertainty.
            </h2>
          </div>
          <div className="border-t border-emerald-400/15 p-9 sm:p-14 lg:border-l lg:border-t-0">
            <ul className="space-y-5 text-white/70">
              <li>• No invented tariffs, savings or sources</li>
              <li>• Weather presented as context, not confirmed causation</li>
              <li>• Unsafe electrical instructions blocked</li>
              <li>• Confidence, sources, agents and safety notes visible</li>
              <li>• Private records scoped to the authenticated user</li>
            </ul>
          </div>
        </div>
      </section>


      <section className="relative border-t border-white/10 px-6 py-28 text-center">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_center,rgba(52,211,153,0.14),transparent_42%)]" />
        <p className="text-sm font-medium uppercase tracking-[0.22em] text-emerald-300">
          Your energy story starts with your data
        </p>
        <h2 className="mx-auto mt-5 max-w-4xl text-4xl font-semibold tracking-[-0.04em] sm:text-6xl">
          Make the next solar decision with a clearer view.
        </h2>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-white/55">
          Create a private HelioSL profile or return to your dashboard.
        </p>
        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <Link
            href="/register"
            className="rounded-2xl bg-emerald-400 px-7 py-4 font-semibold text-[#06110d] transition hover:bg-emerald-300"
          >
            Get started
          </Link>
          <Link
            href="/login"
            className="rounded-2xl border border-white/15 px-7 py-4 font-medium transition hover:bg-white/5"
          >
            Log in
          </Link>
        </div>
      </section>


      <footer className="border-t border-white/10 px-6 py-8 text-sm text-white/38">
        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-5 sm:flex-row lg:px-2">
          <p>© 2026 HelioSL · Academic renewable-energy decision support.</p>
          <div className="flex flex-wrap gap-5">
            <a
              href="https://www.pucsl.gov.lk/wp-content/uploads/2026/03/Analysis-on-Rooftop-Solar-Integration-Industry-Growth-in-Sri-Lanka.pdf"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white"
            >
              PUCSL data source
            </a>
            <a
              href="https://www.energy.gov.lk/en/renewable-energy/technologies/solar-energy"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white"
            >
              SLSEA solar information
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}


function Stat({
  value,
  label,
}: {
  value: string;
  label: string;
}) {
  return (
    <div className="px-6 py-9 text-center">
      <p className="text-3xl font-semibold text-emerald-300">
        {value}
      </p>
      <p className="mt-2 text-sm text-white/45">
        {label}
      </p>
    </div>
  );
}


function PhotoCard({
  src,
  alt,
  eyebrow,
  title,
  className = "",
}: {
  src: string;
  alt: string;
  eyebrow: string;
  title: string;
  className?: string;
}) {
  return (
    <article
      className={`group relative min-h-[390px] overflow-hidden rounded-[1.75rem] border border-white/10 ${className}`}
    >
      <Image
        src={src}
        alt={alt}
        fill
        unoptimized
        sizes="(max-width: 640px) 90vw, (max-width: 1024px) 45vw, 28vw"
        className="object-cover transition duration-700 group-hover:scale-105"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/15 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 p-6">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-300">
          {eyebrow}
        </p>
        <h3 className="mt-3 text-xl font-semibold leading-7">
          {title}
        </h3>
      </div>
    </article>
  );
}
