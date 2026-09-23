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
  getEnergyProfile,
} from "@/services/energy-service";

import {
  getSolarSystem,
} from "@/services/solar-service";

import type {
  User,
} from "@/types/user";

import type {
  EnergyProfile,
} from "@/types/energy";

import type {
  SolarSystem,
} from "@/types/solar";


export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] =
    useState<User | null>(null);

  const [energyProfile, setEnergyProfile] =
    useState<EnergyProfile | null>(null);

  const [solarSystem, setSolarSystem] =
    useState<SolarSystem | null>(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.replace("/login");
      return;
    }

    async function loadUser() {
      try {
        // Load current user
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);


        // Load energy profile
        try {
          const energy =
            await getEnergyProfile();

          setEnergyProfile(energy);
        } catch {
          setEnergyProfile(null);
        }


        // Load solar system
        try {
          const solar =
            await getSolarSystem();

          setSolarSystem(solar);
        } catch {
          setSolarSystem(null);
        }

      } catch {
        removeToken();
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }

    loadUser();
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


      <div className="mt-10 grid gap-5 md:grid-cols-3">

        {/* Monthly Consumption */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            Monthly Consumption
          </p>

          <p className="mt-3 text-2xl font-semibold text-white">
            {energyProfile?.average_monthly_consumption_kwh
              ? `${energyProfile.average_monthly_consumption_kwh} kWh`
              : "—"}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            {energyProfile
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
            {solarSystem?.capacity_kw
              ? `${solarSystem.capacity_kw} kW`
              : "—"}
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            {solarSystem
              ? "Installed solar system capacity"
              : "Solar system not loaded"}
          </p>
        </div>


        {/* HelioSL AI */}
        <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <p className="text-sm text-neutral-400">
            HelioSL AI
          </p>

          <p className="mt-3 text-2xl font-semibold text-emerald-400">
            Ready
          </p>

          <p className="mt-1 text-sm text-neutral-500">
            Intelligence layer coming soon
          </p>
        </div>

      </div>
    </DashboardShell>
  );
}