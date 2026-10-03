"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";


const DIRECTORY_URL = (
  "https://www.energy.gov.lk/en/soorya-bala-sangramaya"
);

const providersByCity = {
  Colombo: [
    ["OREL Corporation (Pvt) Ltd", "Colombo 02", "S004"],
    ["Abans Electricals PLC", "Colombo 03", "S048"],
  ],
  Gampaha: [
    ["Green Light Solar Lanka (Pvt) Ltd", "Yakkala", "S049"],
    ["Senuk Solar Engineering (Pvt) Ltd", "Gampaha", "S043"],
  ],
  Kandy: [
    ["Extreme Energy (Pvt) Ltd", "Kandy", "S175"],
  ],
  Matara: [
    ["Alta Vision (Pvt) Ltd", "Matara", "S058"],
    ["Simpex Holdings (Pvt) Ltd", "Matara", "S182"],
  ],
  Galle: [
    ["Ferentix (Pvt) Ltd", "Galle", "S991"],
    ["Jaya Hansa Holdings (Pvt) Ltd", "Aluthwala", "S905"],
  ],
  Kurunegala: [
    ["BG Solar Energy (Pvt) Ltd", "Kurunegala", "S110"],
    ["LSD Engineering Solutions (Pvt) Ltd", "Kurunegala", "S708"],
  ],
  Jaffna: [
    ["Ecosteem (Pvt) Ltd", "Jaffna", "S020"],
    ["Sivan Power (Pvt) Ltd", "Kankesanthurai", "S562"],
  ],
  Negombo: [
    ["Sunray Green Energy (Pvt) Ltd", "Negombo", "S900"],
    ["Justech Engineering (Pvt) Ltd", "Kadirana", "S365"],
  ],
} as const;

type City = keyof typeof providersByCity;

type MatchResult = {
  scheme: string;
  reason: string;
  capacity: string;
  nextStep: string;
};


function getCapacityBand(
  usage: string,
  customerType: string
) {
  if (usage === "under-200") return "Around 2 kW to explore";
  if (usage === "200-400") return "Around 3–5 kW to explore";
  if (usage === "400-700") return "Around 5–7 kW to explore";
  if (customerType === "business") return "10–20+ kW site assessment";
  return "7–10+ kW site assessment";
}


function getScheme(
  goal: string,
  roofAccess: string,
  usage: string,
  customerType: string
): MatchResult {
  const capacity = getCapacityBand(
    usage,
    customerType
  );

  if (roofAccess === "shared") {
    return {
      scheme: "Shared-roof or aggregator assessment",
      reason: (
        "Because you do not control the roof alone, ownership, wiring "
        + "and utility approval need to be resolved before choosing a scheme."
      ),
      capacity,
      nextStep: (
        "Discuss written roof permission and ask an SLSEA-registered "
        + "provider whether Net Plus Plus or another approved structure applies."
      ),
    };
  }

  if (goal === "export") {
    return {
      scheme: "Net Plus starting point",
      reason: (
        "Net Plus separates your electricity consumption from solar "
        + "generation and compensates total exported generation under agreed terms."
      ),
      capacity,
      nextStep: "Request a site survey and verify the current utility agreement and tariff.",
    };
  }

  if (goal === "balance") {
    return {
      scheme: "Net Accounting starting point",
      reason: (
        "Net Accounting can support self-use while compensating excess "
        + "energy exported to the grid under the applicable agreement."
      ),
      capacity,
      nextStep: "Compare expected self-consumption with the current export terms.",
    };
  }

  if (goal === "backup") {
    return {
      scheme: "Solar plus BESS assessment",
      reason: (
        "Backup requires a battery and protected-load design; a grid-export "
        + "scheme alone does not provide outage backup."
      ),
      capacity,
      nextStep: "Ask for a qualified load study, battery sizing and safe changeover design.",
    };
  }

  return {
    scheme: "Net Metering starting point",
    reason: (
      "Net Metering is oriented toward offsetting your own use through "
      + "energy credits rather than receiving payment for generation."
    ),
    capacity,
    nextStep: "Compare at least 12 months of bills before selecting capacity.",
  };
}


export function SolarPathFinder() {
  const [customerType, setCustomerType] = useState("household");
  const [city, setCity] = useState<City>("Colombo");
  const [usage, setUsage] = useState("200-400");
  const [goal, setGoal] = useState("reduce");
  const [roofAccess, setRoofAccess] = useState("own");
  const [result, setResult] = useState<MatchResult | null>(null);


  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setResult(
      getScheme(
        goal,
        roofAccess,
        usage,
        customerType
      )
    );
  }


  return (
    <section id="solar-path" className="border-y border-white/10 bg-[#0a1913] py-28">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[0.8fr_1.2fr]">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.22em] text-yellow-200">
              A useful first visit
            </p>
            <h2 className="mt-5 text-4xl font-semibold tracking-[-0.035em] sm:text-5xl">
              Find a practical solar starting point in two minutes.
            </h2>
            <p className="mt-6 text-lg leading-8 text-white/58">
              Tell us only what you are comfortable sharing. HelioSL
              uses your selected city—not live location—to suggest a
              scheme direction, planning band and nearby registered-provider leads.
            </p>

            <div className="mt-8 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.07] p-5 text-sm leading-6 text-emerald-100/75">
              This is a discovery tool, not a quotation or engineering
              recommendation. Current scheme terms, tariffs, roof condition
              and provider registration must be verified before purchase.
            </div>
          </div>

          <div className="rounded-[2rem] border border-white/10 bg-black/20 p-6 sm:p-8">
            <form onSubmit={handleSubmit} className="grid gap-5 sm:grid-cols-2">
              <Select
                label="I am exploring for"
                value={customerType}
                onChange={setCustomerType}
                options={[
                  ["household", "My household"],
                  ["business", "My business"],
                ]}
              />
              <Select
                label="Nearest city"
                value={city}
                onChange={(value) => setCity(value as City)}
                options={Object.keys(providersByCity).map((value) => [value, value])}
              />
              <Select
                label="Approximate monthly use"
                value={usage}
                onChange={setUsage}
                options={[
                  ["under-200", "Under 200 kWh"],
                  ["200-400", "200–400 kWh"],
                  ["400-700", "400–700 kWh"],
                  ["over-700", "Over 700 kWh"],
                ]}
              />
              <Select
                label="Main goal"
                value={goal}
                onChange={setGoal}
                options={[
                  ["reduce", "Reduce my electricity bill"],
                  ["balance", "Use solar and sell excess"],
                  ["export", "Generate mainly for export"],
                  ["backup", "Add outage backup"],
                ]}
              />
              <Select
                label="Roof access"
                value={roofAccess}
                onChange={setRoofAccess}
                options={[
                  ["own", "I control the roof"],
                  ["shared", "Shared or rented roof"],
                ]}
                className="sm:col-span-2"
              />

              <button
                type="submit"
                className="rounded-xl bg-emerald-400 px-6 py-3.5 font-semibold text-[#06110d] transition hover:bg-emerald-300 sm:col-span-2"
              >
                Build my starting path
              </button>
            </form>

            {result && (
              <div className="mt-7 border-t border-white/10 pt-7" aria-live="polite">
                <p className="text-xs uppercase tracking-[0.2em] text-emerald-300">
                  Your preliminary path
                </p>
                <h3 className="mt-3 text-2xl font-semibold">
                  {result.scheme}
                </h3>
                <p className="mt-3 leading-7 text-white/60">
                  {result.reason}
                </p>

                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <ResultCard label="Planning band" value={result.capacity} />
                  <ResultCard label="Next useful step" value={result.nextStep} />
                </div>

                <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold">
                        Registered-provider leads near {city}
                      </p>
                      <p className="mt-1 text-xs text-white/40">
                        Location match only—not a ranking or endorsement.
                      </p>
                    </div>
                    <a
                      href={DIRECTORY_URL}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs font-medium text-emerald-300 underline"
                    >
                      Verify latest SLSEA directory
                    </a>
                  </div>

                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    {providersByCity[city].map(([name, area, registration]) => (
                      <div
                        key={registration}
                        className="rounded-xl border border-white/10 bg-black/20 p-4"
                      >
                        <p className="text-sm font-medium text-white">
                          {name}
                        </p>
                        <p className="mt-2 text-xs text-white/45">
                          {area} · SLSEA {registration}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/register"
                    className="rounded-xl bg-white px-5 py-3 text-sm font-semibold text-[#06110d]"
                  >
                    Save and refine this plan
                  </Link>
                  <a
                    href="https://www.pucsl.gov.lk/rooftop-solar-pv-connection-schemes/"
                    target="_blank"
                    rel="noreferrer"
                    className="rounded-xl border border-white/15 px-5 py-3 text-sm font-medium"
                  >
                    Read official scheme details
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}


function Select({
  label,
  value,
  onChange,
  options,
  className = "",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[][];
  className?: string;
}) {
  return (
    <label className={className}>
      <span className="text-sm text-white/65">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-xl border border-white/10 bg-[#07120e] px-4 py-3 text-sm text-white outline-none focus:border-emerald-400"
      >
        {options.map(([optionValue, optionLabel]) => (
          <option key={optionValue} value={optionValue}>
            {optionLabel}
          </option>
        ))}
      </select>
    </label>
  );
}


function ResultCard({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-emerald-400/15 bg-emerald-400/[0.06] p-4">
      <p className="text-xs uppercase tracking-wide text-emerald-300/70">
        {label}
      </p>
      <p className="mt-2 text-sm leading-6 text-white/75">
        {value}
      </p>
    </div>
  );
}
