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


type PlanningPreset =
  | "household"
  | "business"
  | "custom";


export default function PlanningPage() {
  const [selectedPreset, setSelectedPreset] =
    useState<PlanningPreset>("custom");

  const [monthlyConsumption, setMonthlyConsumption] =
    useState("");

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


  function resetCalculation() {
    setResult(null);
    setError("");
  }


  function applyHouseholdPreset() {
    setSelectedPreset("household");
    setMonthlyConsumption("453.67");
    setCapacity("5");
    setCost("1250000");
    setImportTariff("50");
    setExportRate("27");
    setSpecificYield("1400");
    setSelfConsumption("40");
    resetCalculation();
  }


  function applyBusinessPreset() {
    setSelectedPreset("business");
    setMonthlyConsumption("2114.44");
    setCapacity("20");
    setCost("4200000");
    setImportTariff("55");
    setExportRate("27");
    setSpecificYield("1400");
    setSelfConsumption("70");
    resetCalculation();
  }


  function applyCustomPreset() {
    setSelectedPreset("custom");
    setMonthlyConsumption("");
    setCapacity("");
    setCost("");
    setImportTariff("");
    setExportRate("");
    setSpecificYield("");
    setSelfConsumption("40");
    resetCalculation();
  }


  function updateCustomValue(
    setter: (value: string) => void,
    value: string,
  ) {
    setSelectedPreset("custom");
    setter(value);
    resetCalculation();
  }


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const response =
        await calculateScenario({
          average_monthly_consumption_kwh:
            monthlyConsumption
              ? Number(monthlyConsumption)
              : undefined,

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
          simple payback using your energy profile
          or explicit planning inputs.
        </p>
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-2">

        <form
          onSubmit={handleSubmit}
          className="space-y-5 rounded-2xl border border-neutral-800 bg-neutral-900 p-6"
        >
          <fieldset>
            <legend className="text-sm font-medium text-neutral-200">
              Planning preset
            </legend>

            <div className="mt-3 grid gap-2 sm:grid-cols-3">
              <PresetButton
                active={selectedPreset === "household"}
                label="Household Demo"
                onClick={applyHouseholdPreset}
              />

              <PresetButton
                active={selectedPreset === "business"}
                label="Business Demo"
                onClick={applyBusinessPreset}
              />

              <PresetButton
                active={selectedPreset === "custom"}
                label="Custom"
                onClick={applyCustomPreset}
              />
            </div>

            <p className="mt-3 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-xs leading-5 text-amber-200">
              Synthetic demonstration assumptions only — verify current
              tariffs, installation costs and site yield before real-world
              use. Preset consumption values mirror the synthetic demo
              profiles and are not customer records.
            </p>
          </fieldset>

          <Input
            label="Average monthly consumption (kWh)"
            value={monthlyConsumption}
            setValue={(value) =>
              updateCustomValue(
                setMonthlyConsumption,
                value,
              )
            }
            help="Optional when your energy profile already contains this value."
          />

          <Input
            label="Solar capacity (kW)"
            value={capacity}
            setValue={(value) =>
              updateCustomValue(
                setCapacity,
                value,
              )
            }
          />

          <Input
            label="Installation cost (LKR)"
            value={cost}
            setValue={(value) =>
              updateCustomValue(
                setCost,
                value,
              )
            }
          />

          <Input
            label="Import tariff (LKR/kWh)"
            value={importTariff}
            setValue={(value) =>
              updateCustomValue(
                setImportTariff,
                value,
              )
            }
          />

          <Input
            label="Export rate (LKR/kWh)"
            value={exportRate}
            setValue={(value) =>
              updateCustomValue(
                setExportRate,
                value,
              )
            }
          />

          <Input
            label="Specific solar yield (kWh/kW/year)"
            value={specificYield}
            setValue={(value) =>
              updateCustomValue(
                setSpecificYield,
                value,
              )
            }
          />

          <Input
            label="Estimated self-consumption (%)"
            value={selfConsumption}
            setValue={(value) =>
              updateCustomValue(
                setSelfConsumption,
                value,
              )
            }
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
              <div
                className={`rounded-xl border px-4 py-3 text-sm ${
                  result.calculation_ready
                    ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-300"
                    : "border-amber-500/40 bg-amber-500/10 text-amber-300"
                }`}
              >
                {result.calculation_ready
                  ? "Energy calculation complete"
                  : "Calculation incomplete"}
              </div>

              <Metric
                label="Annual Consumption"
                value={
                  result.annual_consumption_kwh !== null
                    ? `${formatNumber(result.annual_consumption_kwh)} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Estimated Solar Generation"
                value={
                  result.estimated_annual_generation_kwh !== null
                    ? `${formatNumber(result.estimated_annual_generation_kwh)} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Self-consumed Solar"
                value={
                  result.self_consumed_solar_kwh !== null
                    ? `${formatNumber(result.self_consumed_solar_kwh)} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Exported Solar"
                value={
                  result.exported_solar_kwh !== null
                    ? `${formatNumber(result.exported_solar_kwh)} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Grid Import"
                value={
                  result.grid_import_kwh !== null
                    ? `${formatNumber(result.grid_import_kwh)} kWh`
                    : "Unavailable"
                }
              />

              <Metric
                label="Energy Coverage"
                value={
                  result.energy_coverage_percent !== null
                    ? `${formatNumber(result.energy_coverage_percent)}%`
                    : "Unavailable"
                }
              />

              <Metric
                label="Avoided Import Cost"
                value={
                  result.avoided_import_cost_lkr !== null
                    ? `LKR ${formatNumber(result.avoided_import_cost_lkr)}`
                    : "Unavailable"
                }
              />

              <Metric
                label="Export Income"
                value={
                  result.export_income_lkr !== null
                    ? `LKR ${formatNumber(result.export_income_lkr)}`
                    : "Unavailable"
                }
              />

              <Metric
                label="Estimated Annual Benefit"
                value={
                  result.estimated_annual_benefit_lkr !== null
                    ? `LKR ${formatNumber(result.estimated_annual_benefit_lkr)}`
                    : "Unavailable"
                }
              />

              <Metric
                label="Simple Payback"
                value={
                  result.simple_payback_years !== null
                    ? `${formatNumber(result.simple_payback_years)} years`
                    : "Unavailable"
                }
              />

              {!result.financial_calculation_ready && (
                <p className="rounded-xl border border-neutral-700 bg-neutral-950 px-4 py-3 text-sm text-neutral-400">
                  Financial estimates are unavailable until all required financial inputs are provided.
                </p>
              )}

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


function PresetButton({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={`rounded-xl border px-3 py-2 text-sm font-medium transition ${
        active
          ? "border-emerald-400 bg-emerald-400/15 text-emerald-300"
          : "border-neutral-700 bg-neutral-950 text-neutral-300 hover:border-neutral-500"
      }`}
    >
      {label}
    </button>
  );
}


function Input({
  label,
  value,
  setValue,
  help,
}: {
  label: string;
  value: string;
  setValue: (value: string) => void;
  help?: string;
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

      {help && (
        <p className="mt-2 text-xs text-neutral-500">
          {help}
        </p>
      )}
    </div>
  );
}


function formatNumber(value: number) {
  return new Intl.NumberFormat("en-LK", {
    maximumFractionDigits: 2,
  }).format(value);
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
