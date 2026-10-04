"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { LoadingScreen } from "@/components/ui/loading-screen";
import { getToken, removeToken } from "@/lib/auth";
import { getCurrentUser, updateCurrentUser } from "@/services/auth-service";
import type { User } from "@/types/user";


const fieldClass =
  "mt-2 w-full rounded-xl border border-neutral-700 bg-neutral-950 px-4 py-3 text-white outline-none transition focus:border-emerald-400/60 focus:ring-4 focus:ring-emerald-400/10 disabled:cursor-not-allowed disabled:opacity-55";


export default function SettingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [fullName, setFullName] = useState("");
  const [district, setDistrict] = useState("");
  const [userType, setUserType] = useState<"household" | "business">("household");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }

    getCurrentUser()
      .then((currentUser) => {
        setUser(currentUser);
        setFullName(currentUser.full_name);
        setDistrict(currentUser.district ?? "");
        setUserType(currentUser.user_type === "business" ? "business" : "household");
      })
      .catch(() => {
        removeToken();
        router.replace("/login");
      })
      .finally(() => setLoading(false));
  }, [router]);

  async function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      const updated = await updateCurrentUser({
        full_name: fullName.trim(),
        district: district.trim() || null,
        user_type: userType,
      });
      setUser(updated);
      setMessage("Your profile has been updated.");
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Unable to update your profile.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <LoadingScreen label="Loading your account settings" />;

  return (
    <DashboardShell>
      <div className="mx-auto max-w-4xl">
        <p className="text-sm text-neutral-400">Account</p>
        <h1 className="mt-2 text-3xl font-semibold text-white">Settings</h1>
        <p className="mt-2 text-neutral-400">Keep your HelioSL profile accurate and review your account information.</p>

        <div className="mt-9 grid gap-6 lg:grid-cols-[1fr_0.55fr]">
          <form onSubmit={saveProfile} className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6 sm:p-8">
            <h2 className="text-lg font-semibold text-white">Profile information</h2>
            <p className="mt-2 text-sm text-neutral-500">These details help tailor your dashboard and energy context.</p>

            <div className="mt-6 space-y-5">
              <div>
                <label htmlFor="settings-name" className="text-sm text-neutral-300">Full name</label>
                <input id="settings-name" value={fullName} onChange={(event) => setFullName(event.target.value)} required minLength={2} className={fieldClass} />
              </div>

              <div>
                <label htmlFor="settings-email" className="text-sm text-neutral-300">Email address</label>
                <input id="settings-email" value={user?.email ?? ""} disabled className={fieldClass} />
                <p className="mt-2 text-xs text-neutral-600">Email changes are protected and not available in the Alpha release.</p>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="settings-district" className="text-sm text-neutral-300">District</label>
                  <input id="settings-district" value={district} onChange={(event) => setDistrict(event.target.value)} className={fieldClass} />
                </div>
                <div>
                  <label htmlFor="settings-type" className="text-sm text-neutral-300">Profile type</label>
                  <select id="settings-type" value={userType} onChange={(event) => setUserType(event.target.value as "household" | "business")} className={fieldClass}>
                    <option value="household">Household</option>
                    <option value="business">Business</option>
                  </select>
                </div>
              </div>
            </div>

            {message && <p className="mt-5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300">{message}</p>}
            {error && <p role="alert" className="mt-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">{error}</p>}

            <button type="submit" disabled={saving} className="mt-6 rounded-xl bg-emerald-400 px-5 py-3 text-sm font-semibold text-neutral-950 transition hover:bg-emerald-300 disabled:opacity-50">
              {saving ? "Saving changes..." : "Save profile"}
            </button>
          </form>

          <aside className="space-y-5">
            <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
              <p className="text-xs uppercase tracking-wider text-neutral-500">Current plan</p>
              <p className="mt-3 text-xl font-semibold text-white">HelioSL Alpha</p>
              <p className="mt-2 text-sm leading-6 text-neutral-500">Core energy intelligence and responsible AI features for early users.</p>
            </div>
            <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
              <p className="text-xs uppercase tracking-wider text-neutral-500">Account status</p>
              <p className="mt-3 text-sm font-medium text-emerald-300">{user?.is_active ? "● Active" : "Inactive"}</p>
              <p className="mt-3 text-xs text-neutral-600">Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "—"}</p>
            </div>
          </aside>
        </div>
      </div>
    </DashboardShell>
  );
}
