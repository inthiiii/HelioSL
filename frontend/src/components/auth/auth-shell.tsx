import type { ReactNode } from "react";

import { HelioLogo } from "@/components/brand/helio-logo";


interface AuthShellProps {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
  footer: ReactNode;
}


export function AuthShell({
  eyebrow,
  title,
  description,
  children,
  footer,
}: AuthShellProps) {
  return (
    <main className="min-h-screen bg-[#06110d] text-white lg:grid lg:grid-cols-[0.92fr_1.08fr]">
      <section className="relative hidden overflow-hidden border-r border-white/10 p-12 lg:flex lg:flex-col xl:p-16">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_18%,rgba(52,211,153,0.24),transparent_34%),radial-gradient(circle_at_80%_80%,rgba(250,204,21,0.12),transparent_34%)]" />
        <div className="relative z-10">
          <HelioLogo />
        </div>

        <div className="relative z-10 my-auto max-w-xl py-16">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-300">
            Energy decisions, made clearer
          </p>
          <h2 className="mt-6 text-5xl font-semibold leading-[1.06] tracking-[-0.045em] xl:text-6xl">
            Your energy story deserves more than guesswork.
          </h2>
          <p className="mt-6 max-w-lg text-lg leading-8 text-white/58">
            Understand consumption, monitor solar, explore planning scenarios
            and ask an accountable AI assistant built around Sri Lankan needs.
          </p>

          <div className="mt-10 grid gap-3 sm:grid-cols-2">
            {[
              "Private, user-scoped records",
              "Transparent AI reasoning",
              "Sri Lankan energy context",
              "Responsible planning support",
            ].map((item) => (
              <div
                key={item}
                className="rounded-2xl border border-white/10 bg-white/[0.045] p-4 text-sm text-white/72 backdrop-blur"
              >
                <span className="mr-2 text-emerald-300">✓</span>
                {item}
              </div>
            ))}
          </div>
        </div>

        <p className="relative z-10 text-xs text-white/35">
          Renewable-energy intelligence for households and businesses.
        </p>
      </section>

      <section className="relative flex min-h-screen items-center justify-center px-5 py-10 sm:px-8 lg:px-12">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_85%_10%,rgba(52,211,153,0.10),transparent_30%)] lg:hidden" />
        <div className="relative w-full max-w-xl">
          <div className="mb-10 flex justify-center lg:hidden">
            <HelioLogo />
          </div>

          <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-6 shadow-2xl shadow-black/25 backdrop-blur sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-300">
              {eyebrow}
            </p>
            <h1 className="mt-3 text-3xl font-semibold tracking-[-0.03em] sm:text-4xl">
              {title}
            </h1>
            <p className="mt-3 text-sm leading-6 text-white/50">
              {description}
            </p>

            <div className="mt-8">{children}</div>
            <div className="mt-7 border-t border-white/10 pt-6 text-center text-sm text-white/48">
              {footer}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
