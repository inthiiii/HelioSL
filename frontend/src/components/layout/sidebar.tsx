"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { HelioLogo } from "@/components/brand/helio-logo";
import { removeToken } from "@/lib/auth";


const navigation = [
  { name: "Overview", shortName: "Overview", href: "/dashboard", icon: "⌂" },
  { name: "Energy", shortName: "Energy", href: "/energy", icon: "↗" },
  { name: "Import Bill", shortName: "Bills", href: "/energy/bills", icon: "▤" },
  { name: "Solar", shortName: "Solar", href: "/solar", icon: "☀" },
  { name: "Solar Planner", shortName: "Planner", href: "/planning", icon: "◇" },
  { name: "AI Assistant", shortName: "Assistant", href: "/assistant", icon: "✦" },
];


export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [upgradeOpen, setUpgradeOpen] = useState(false);
  const [planType, setPlanType] = useState<"home" | "business">("home");

  useEffect(() => {
    if (!upgradeOpen) return;

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") setUpgradeOpen(false);
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [upgradeOpen]);

  function logout() {
    removeToken();
    router.push("/login");
  }

  return (
    <>
      <aside className="z-30 flex w-full shrink-0 flex-col border-b border-neutral-800 bg-neutral-950 px-4 py-4 lg:sticky lg:top-0 lg:h-screen lg:w-64 lg:border-b-0 lg:border-r lg:p-5">
        <div className="flex items-center justify-between lg:block">
          <HelioLogo />
          <span className="rounded-full border border-white/10 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-white/45 lg:mt-5 lg:inline-flex">
            Alpha · Current plan
          </span>
        </div>

        <nav className="mt-4 flex gap-2 overflow-x-auto pb-1 lg:mt-7 lg:block lg:space-y-1.5 lg:overflow-visible lg:pb-0">
          {navigation.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex shrink-0 items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm transition lg:w-full ${
                  active
                    ? "bg-emerald-400/12 text-emerald-300 ring-1 ring-emerald-400/20"
                    : "text-neutral-400 hover:bg-neutral-900 hover:text-white"
                }`}
              >
                <span className="grid h-6 w-6 place-items-center text-base" aria-hidden="true">{item.icon}</span>
                <span className="lg:hidden">{item.shortName}</span>
                <span className="hidden lg:inline">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-4 flex gap-2 border-t border-neutral-800 pt-4 lg:mt-auto lg:block lg:space-y-2">
          <button
            type="button"
            onClick={() => setUpgradeOpen(true)}
            className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-400 to-yellow-300 px-4 py-2.5 text-sm font-semibold text-neutral-950 transition hover:brightness-105 lg:w-full"
          >
            <span aria-hidden="true">↗</span>
            Upgrade
          </button>
          <Link
            href="/settings"
            className={`flex flex-1 items-center justify-center gap-2 rounded-xl border px-4 py-2.5 text-sm transition lg:w-full ${
              pathname === "/settings"
                ? "border-emerald-400/30 bg-emerald-400/10 text-emerald-300"
                : "border-neutral-800 text-neutral-300 hover:bg-neutral-900"
            }`}
          >
            <span aria-hidden="true">⚙</span>
            Settings
          </Link>
          <button
            type="button"
            onClick={logout}
            className="rounded-xl border border-neutral-800 px-4 py-2.5 text-sm text-neutral-400 transition hover:bg-neutral-900 hover:text-white lg:w-full"
          >
            Log out
          </button>
        </div>
      </aside>

      {upgradeOpen && (
        <div
          className="fixed inset-0 z-50 grid place-items-center bg-black/65 px-5 py-8 backdrop-blur-md"
          role="presentation"
          onMouseDown={(event) => {
            if (event.currentTarget === event.target) setUpgradeOpen(false);
          }}
        >
          <section
            role="dialog"
            aria-modal="true"
            aria-labelledby="upgrade-title"
            className="relative w-full max-w-2xl overflow-hidden rounded-[2rem] border border-white/12 bg-[#0b1712] p-6 shadow-2xl sm:p-9"
          >
            <button
              type="button"
              onClick={() => setUpgradeOpen(false)}
              className="absolute right-5 top-5 grid h-9 w-9 place-items-center rounded-full border border-white/10 text-white/55 hover:bg-white/10 hover:text-white"
              aria-label="Close upgrade options"
            >
              ×
            </button>

            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-300">Coming next</p>
            <h2 id="upgrade-title" className="mt-3 text-3xl font-semibold tracking-tight text-white">
              Grow with HelioSL Pro
            </h2>
            <p className="mt-3 max-w-xl text-sm leading-6 text-white/48">
              You are currently using the HelioSL Alpha experience. Preview future plans designed for deeper household and business intelligence.
            </p>

            <div className="mt-7 grid grid-cols-2 rounded-xl border border-white/10 bg-black/20 p-1">
              {(["home", "business"] as const).map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setPlanType(type)}
                  className={`rounded-lg px-4 py-2.5 text-sm font-semibold capitalize transition ${
                    planType === type ? "bg-emerald-400 text-[#06110d]" : "text-white/48 hover:text-white"
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>

            <div className="mt-5 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.06] p-6">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-sm text-emerald-300">{planType === "home" ? "Home Pro" : "Business Pro"}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">
                    {planType === "home" ? "LKR 1,500" : "LKR 30,000"}
                    <span className="text-sm font-normal text-white/40"> / month</span>
                  </p>
                  <p className="mt-1 text-xs text-white/40">
                    {planType === "home" ? "or LKR 15,000 / year" : "or contact us for a custom plan"}
                  </p>
                </div>
                <span className="rounded-full border border-yellow-300/20 bg-yellow-300/10 px-3 py-1 text-xs font-semibold text-yellow-200">Preview</span>
              </div>

              <ul className="mt-6 grid gap-3 text-sm text-white/65 sm:grid-cols-2">
                {(planType === "home"
                  ? ["Deeper household forecasts", "Personal energy goals", "Priority AI insights", "Extended record history"]
                  : ["Multi-site intelligence", "Team access and roles", "Advanced reporting", "Custom data integration"]
                ).map((benefit) => <li key={benefit}>✓ {benefit}</li>)}
              </ul>

              <button
                type="button"
                disabled
                className="mt-7 w-full rounded-xl bg-white/10 px-4 py-3 text-sm font-semibold text-white/45"
              >
                Available in a future release
              </button>
            </div>
          </section>
        </div>
      )}
    </>
  );
}
