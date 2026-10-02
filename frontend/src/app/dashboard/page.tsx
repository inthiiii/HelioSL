"use client";

import {
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

      try {
        const integratedSummary =
          await getIntegratedSummary();

        setSummary(integratedSummary);
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load the integrated summary."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [router]);


  if (loading) {
    return (
      <main className="min-h-screen bg-neutral-950 p-10 text-white">
        Loading HelioSL...
      </main>
    );
  }


  return (
    <DashboardShell>
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


      <section className="mt-8 rounded-2xl border border-amber-900/60 bg-amber-950/20 p-6">
        <h2 className="text-lg font-semibold text-white">
          HelioSL Insights
        </h2>

        <p className="mt-1 text-sm text-neutral-400">
          Observations from your available energy and solar records.
          These are indicators, not definitive fault diagnoses.
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
    </DashboardShell>
  );
}
