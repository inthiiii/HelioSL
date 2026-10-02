"use client";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  useRouter,
} from "next/navigation";

import { DashboardShell } from "@/components/layout/dashboard-shell";

import {
  getToken,
  removeToken,
} from "@/lib/auth";

import {
  getCurrentUser,
} from "@/services/auth-service";

import {
  getIntegratedSummary,
} from "@/services/integration-service";

import type {
  User,
} from "@/types/user";

import type {
  IntegratedSummary,
} from "@/types/integration";


function formatNumber(
  value: unknown,
  unit: string,
) {
  if (typeof value !== "number") {
    return "—";
  }

  return `${value.toLocaleString(undefined, {
    maximumFractionDigits: 2,
  })} ${unit}`;
}


function formatLabel(value: unknown) {
  if (typeof value !== "string" || !value) {
    return "—";
  }

  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase()
    );
}


export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] =
    useState<User | null>(null);

  const [summary, setSummary] =
    useState<IntegratedSummary | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [refreshing, setRefreshing] =
    useState(false);

  const [lastUpdated, setLastUpdated] =
    useState<Date | null>(null);


  const refreshSummary = useCallback(
    async (showProgress = true) => {
      if (showProgress) {
        setRefreshing(true);
      }

      try {
        const integratedSummary =
          await getIntegratedSummary();

        setSummary(integratedSummary);
        setLastUpdated(new Date());
        setError("");
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load the integrated summary."
        );
      } finally {
        if (showProgress) {
          setRefreshing(false);
        }
      }
    },
    [],
  );


  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.replace("/login");
      return;
    }

    async function loadDashboard() {
      try {
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);
      } catch {
        removeToken();
        router.replace("/login");
        return;
      }

      await refreshSummary(false);
      setLoading(false);
    }

    loadDashboard();

    const refreshInterval = window.setInterval(
      () => refreshSummary(false),
      5 * 60 * 1000,
    );

    return () => {
      window.clearInterval(refreshInterval);
    };
  }, [refreshSummary, router]);


  if (loading) {
    return (
      <main className="min-h-screen bg-neutral-950 p-10 text-white">
        Loading HelioSL...
      </main>
    );
  }


  return (
    <DashboardShell>
      <div className="flex flex-wrap items-end justify-between gap-5">
        <div>
          <p className="text-sm text-neutral-400">
            Overview
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            Welcome, {user?.full_name}
          </h1>

          <p className="mt-2 text-neutral-400">
            Your renewable energy intelligence dashboard.
          </p>
        </div>

        <div className="text-right">
          <button
            type="button"
            disabled={refreshing}
            onClick={() => refreshSummary()}
            className="rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-4 py-2 text-sm font-medium text-emerald-300 transition hover:bg-emerald-500/20 disabled:opacity-50"
          >
            {refreshing ? "Refreshing..." : "Refresh live data"}
          </button>

          <p className="mt-2 text-xs text-neutral-500">
            {lastUpdated
              ? `Updated ${lastUpdated.toLocaleTimeString()}`
              : "Waiting for live data"}
          </p>
        </div>
      </div>


      {error ? (
        <div
          className="mt-8 rounded-2xl border border-red-900/70 bg-red-950/40 p-5 text-sm text-red-200"
          role="alert"
        >
          {error}
        </div>
      ) : null}


      <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-5">

        {/* User Type */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            User Type
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {formatLabel(summary?.user_type)}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            {summary?.district ?? "District not provided"}
          </p>
        </div>

        {/* Average Consumption */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Average Consumption
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {formatNumber(
              summary?.energy.average_consumption_kwh,
              "kWh"
            )}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            {summary?.energy_profile_available
              ? "Average monthly electricity usage"
              : "Energy profile not loaded"}
          </p>
        </div>


        {/* Solar Capacity */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Solar Capacity
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {formatNumber(
              summary?.solar.capacity_kw,
              "kW"
            )}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            {summary?.solar_system_available
              ? "Installed solar system capacity"
              : "Solar system not loaded"}
          </p>
        </div>


        {/* Consumption Trend */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Consumption Trend
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {formatLabel(
              summary?.energy.consumption_trend
            )}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            Based on available consumption records
          </p>
        </div>


        {/* Solar Generation Trend */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Solar Generation Trend
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {formatLabel(
              summary?.energy.generation_trend
            )}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            Based on available generation records
          </p>
        </div>

      </div>


      <section className="mt-8 overflow-hidden rounded-2xl border border-sky-500/20 bg-gradient-to-br from-sky-950/60 via-neutral-900 to-emerald-950/40 p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-sky-300">
              Live environmental context
            </p>

            <h2 className="mt-2 text-xl font-semibold text-white">
              Weather in {summary?.district ?? "your district"}
            </h2>
          </div>

          <span className="rounded-full border border-sky-400/30 bg-sky-400/10 px-3 py-1 text-xs text-sky-200">
            {summary?.weather.available ? "Live" : "Unavailable"}
          </span>
        </div>

        {summary?.weather.available ? (
          <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
            <WeatherMetric
              label="Temperature"
              value={formatNumber(
                summary.weather.temperature_c,
                "°C"
              )}
            />
            <WeatherMetric
              label="Humidity"
              value={formatNumber(
                summary.weather.humidity_percent,
                "%"
              )}
            />
            <WeatherMetric
              label="Cloud cover"
              value={formatNumber(
                summary.weather.cloud_cover_percent,
                "%"
              )}
            />
            <WeatherMetric
              label="Precipitation"
              value={formatNumber(
                summary.weather.precipitation_mm,
                "mm"
              )}
            />
            <WeatherMetric
              label="Solar radiation"
              value={formatNumber(
                summary.weather.shortwave_radiation_sum,
                "MJ/m²"
              )}
            />
          </div>
        ) : (
          <p className="mt-5 text-sm text-neutral-400">
            {typeof summary?.weather.reason === "string"
              ? summary.weather.reason
              : "Live weather is temporarily unavailable."}
          </p>
        )}

        <p className="mt-5 text-xs leading-5 text-neutral-500">
          Live conditions can provide context for short-term output,
          but they do not prove the cause of historical performance changes.
        </p>
      </section>


      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-amber-900/60 bg-amber-950/20 p-6">
          <h2 className="text-lg font-semibold text-white">
            HelioSL Insights
          </h2>

          <p className="mt-1 text-sm text-neutral-400">
            Data observations—not definitive fault diagnoses.
          </p>

          {summary?.alerts.length ? (
            <ul className="mt-5 space-y-3">
              {summary.alerts.map((alert) => (
                <li
                  className="flex gap-3 text-sm text-amber-100"
                  key={alert}
                >
                  <span aria-hidden="true">⚠</span>
                  <span>{alert}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-5 text-sm text-neutral-400">
              No trend-based insights are currently available.
            </p>
          )}
        </section>

        <section className="rounded-2xl border border-emerald-900/60 bg-emerald-950/20 p-6">
          <h2 className="text-lg font-semibold text-white">
            Practical tips
          </h2>

          <p className="mt-1 text-sm text-neutral-400">
            Suggestions adapt to your latest records and conditions.
          </p>

          <ul className="mt-5 space-y-3">
            {summary?.tips.map((tip) => (
              <li
                className="flex gap-3 text-sm leading-6 text-emerald-100"
                key={tip}
              >
                <span aria-hidden="true">→</span>
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </DashboardShell>
  );
}


function WeatherMetric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-black/20 p-4">
      <p className="text-xs text-neutral-400">
        {label}
      </p>

      <p className="mt-2 text-lg font-semibold text-white">
        {value}
      </p>
    </div>
  );
}
