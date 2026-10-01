"use client";

import {
  FormEvent,
  useState,
} from "react";

import { DashboardShell } from "@/components/layout/dashboard-shell";

import {
  calculateScenario,
} from "@/services/planning-service";

import type {
  PlanningScenario,
} from "@/types/planning";


export default function PlanningPage() {
  const [capacity, setCapacity] =
    useState("5");

  const [cost, setCost] =
    useState("");

  const [importTariff, setImportTariff] =
    useState("");

  const [exportRate, setExportRate] =
    useState("");

  const [specificYield, setSpecificYield] =
    useState("");

  const [selfConsumption, setSelfConsumption] =
    useState("40");

  const [result, setResult] =
    useState<PlanningScenario | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const response =
        await calculateScenario({
          system_capacity_kw:
            Number(capacity),

          installation_cost_lkr:
            cost
              ? Number(cost)
              : undefined,

          import_tariff_lkr_per_kwh:
            importTariff
              ? Number(importTariff)
              : undefined,

          export_rate_lkr_per_kwh:
            exportRate
              ? Number(exportRate)
              : undefined,

          specific_yield_kwh_per_kw_year:
            specificYield
              ? Number(specificYield)
              : undefined,

          self_consumption_ratio:
            Number(selfConsumption) / 100,
        });

      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Planning calculation failed"
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <DashboardShell>
      <div>
        <p className="text-sm text-neutral-400">
          Solar Planning
        </p>

        <h1 className="mt-2 text-3xl font-semibold text-white">
          Solar & Financial Planner
        </h1>

        <p className="mt-2 max-w-2xl text-neutral-400">
          Explore estimated solar generation,
          electricity coverage, savings and
          simple payback using your energy profile.
        </p>
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-2">

        <form
          onSubmit={handleSubmit}
          className="space-y-5 rounded-2xl border border-neutral-800 bg-neutral-900 p-6"
        >
          <Input
            label="Solar capacity (kW)"
            value={capacity}
            setValue={setCapacity}
          />

          <Input
            label="Installation cost (LKR)"
            value={cost}
            setValue={setCost}
          />

          <Input
            label="Import tariff (LKR/kWh)"
            value={importTariff}
            setValue={setImportTariff}
          />

          <Input
            label="Export rate (LKR/kWh)"
            value={exportRate}
            setValue={setExportRate}
          />

          <Input
            label="Specific solar yield (kWh/kW/year)"
            value={specificYield}
            setValue={setSpecificYield}
          />

          <Input
            label="Estimated self-consumption (%)"
            value={selfConsumption}
            setValue={setSelfConsumption}
          />

          {error && (
            <p className="text-sm text-red-400">
              {error}
            </p>
          )}

          <button
            disabled={loading}
            className="w-full rounded-xl bg-emerald-500 px-5 py-3 font-medium text-black disabled:opacity-50"
          >
            {loading
              ? "Calculating..."
              : "Calculate scenario"}
          </button>
        </form>

        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          {!result ? (
            <p className="text-neutral-400">
              Enter your planning assumptions
              to calculate a scenario.
            </p>
          ) : (
            <div className="space-y-5">

              <Metric
                label="Annual Consumption"
                value={
                  result.annual_consumption_kwh
                    ? `${result.annual_consumption_kwh} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Estimated Solar Generation"
                value={
                  result.estimated_annual_generation_kwh
                    ? `${result.estimated_annual_generation_kwh} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Energy Coverage"
                value={
                  result.energy_coverage_percent
                    ? `${result.energy_coverage_percent}%`
                    : "Unavailable"
                }
              />

              <Metric
                label="Estimated Annual Benefit"
                value={
                  result.estimated_annual_benefit_lkr
                    ? `LKR ${result.estimated_annual_benefit_lkr}`
                    : "Unavailable"
                }
              />

              <Metric
                label="Simple Payback"
                value={
                  result.simple_payback_years
                    ? `${result.simple_payback_years} years`
                    : "Unavailable"
                }
              />

              {result.missing_inputs.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-amber-400">
                    Missing inputs
                  </p>

                  <ul className="mt-2 list-disc pl-5 text-sm text-neutral-400">
                    {result.missing_inputs.map(
                      (item) => (
                        <li key={item}>
                          {item}
                        </li>
                      )
                    )}
                  </ul>
                </div>
              )}

              <p className="text-xs text-neutral-500">
                These values are planning estimates,
                not engineering or financial guarantees.
              </p>
            </div>
          )}
        </div>
      </div>
    </DashboardShell>
  );
}


function Input({
  label,
  value,
  setValue,
}: {
  label: string;
  value: string;
  setValue: (value: string) => void;
}) {
  return (
    <div>
      <label className="text-sm text-neutral-300">
        {label}
      </label>

      <input
        type="number"
        step="any"
        value={value}
        onChange={(event) =>
          setValue(event.target.value)
        }
        className="mt-2 w-full rounded-xl border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
      />
    </div>
  );
}


function Metric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="border-b border-neutral-800 pb-4">
      <p className="text-sm text-neutral-400">
        {label}
      </p>

      <p className="mt-1 text-xl font-semibold text-white">
        {value}
      </p>
    </div>
  );
}