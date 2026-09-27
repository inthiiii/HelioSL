"use client";

import { useEffect, useState } from "react";

import { DashboardShell } from "@/components/layout/dashboard-shell";

import {
  getConsumptionRecords,
  getEnergyProfile,
} from "@/services/energy-service";

import type {
  ConsumptionRecord,
  EnergyProfile,
} from "@/types/energy";


export default function EnergyPage() {
  const [profile, setProfile] =
    useState<EnergyProfile | null>(null);

  const [records, setRecords] =
    useState<ConsumptionRecord[]>([]);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {
    async function loadData() {
      try {
        const energyProfile =
          await getEnergyProfile();

        setProfile(energyProfile);
      } catch {
        setProfile(null);
      }

      try {
        const consumption =
          await getConsumptionRecords();

        setRecords(consumption);
      } catch {
        setRecords([]);
      }

      setLoading(false);
    }

    loadData();
  }, []);


  if (loading) {
    return (
      <DashboardShell>
        <p className="text-white">
          Loading energy data...
        </p>
      </DashboardShell>
    );
  }


  return (
    <DashboardShell>
      <div>
        <p className="text-sm text-neutral-400">
          Energy
        </p>

        <h1 className="mt-2 text-3xl font-semibold text-white">
          Energy Overview
        </h1>

        <p className="mt-2 text-neutral-400">
          Understand your electricity consumption and costs.
        </p>
      </div>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Average Consumption
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {profile?.average_monthly_consumption_kwh
              ? `${profile.average_monthly_consumption_kwh} kWh`
              : "—"}
          </p>
        </div>

        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Average Bill
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {profile?.average_monthly_bill_lkr
              ? `LKR ${profile.average_monthly_bill_lkr}`
              : "—"}
          </p>
        </div>

        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Provider
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {profile?.provider ?? "—"}
          </p>
        </div>
      </div>

      <div className="mt-8 rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
        <h2 className="text-xl font-semibold text-white">
          Consumption History
        </h2>

        {records.length === 0 ? (
          <p className="mt-5 text-neutral-400">
            No consumption records available yet.
          </p>
        ) : (
          <div className="mt-5 space-y-3">
            {records.map((record) => (
              <div
                key={record.id}
                className="flex items-center justify-between border-b border-neutral-800 pb-3"
              >
                <span className="text-neutral-300">
                  {record.billing_month}
                </span>

                <span className="font-medium text-white">
                  {record.consumption_kwh} kWh
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardShell>
  );
}