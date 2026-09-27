"use client";

import { useEffect, useState } from "react";

import { DashboardShell } from "@/components/layout/dashboard-shell";

import {
  getSolarGeneration,
  getSolarSystem,
} from "@/services/solar-service";

import type {
  SolarGenerationRecord,
  SolarSystem,
} from "@/types/solar";


export default function SolarPage() {
  const [system, setSystem] =
    useState<SolarSystem | null>(null);

  const [generation, setGeneration] =
    useState<SolarGenerationRecord[]>([]);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {
    async function loadData() {
      try {
        setSystem(
          await getSolarSystem()
        );
      } catch {
        setSystem(null);
      }

      try {
        setGeneration(
          await getSolarGeneration()
        );
      } catch {
        setGeneration([]);
      }

      setLoading(false);
    }

    loadData();
  }, []);


  if (loading) {
    return (
      <DashboardShell>
        <p className="text-white">
          Loading solar data...
        </p>
      </DashboardShell>
    );
  }


  return (
    <DashboardShell>
      <div>
        <p className="text-sm text-neutral-400">
          Solar
        </p>

        <h1 className="mt-2 text-3xl font-semibold text-white">
          Solar Intelligence
        </h1>

        <p className="mt-2 text-neutral-400">
          Monitor your rooftop solar system and generation.
        </p>
      </div>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            System Capacity
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {system?.capacity_kw
              ? `${system.capacity_kw} kW`
              : "—"}
          </p>
        </div>

        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Scheme
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {system?.scheme ?? "—"}
          </p>
        </div>

        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Installer
          </p>

          <p className="mt-3 text-xl font-semibold text-white">
            {system?.installer_name ?? "—"}
          </p>
        </div>
      </div>

      <div className="mt-8 rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
        <h2 className="text-xl font-semibold text-white">
          Generation History
        </h2>

        {generation.length === 0 ? (
          <p className="mt-5 text-neutral-400">
            No solar generation records available.
          </p>
        ) : (
          <div className="mt-5 space-y-3">
            {generation.map((record) => (
              <div
                key={record.id}
                className="flex justify-between border-b border-neutral-800 pb-3"
              >
                <span className="text-neutral-300">
                  {record.generation_month}
                </span>

                <span className="font-medium text-emerald-400">
                  {record.generation_kwh} kWh
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardShell>
  );
}