"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { AuthShell } from "@/components/auth/auth-shell";
import { registerUser } from "@/services/auth-service";


const fieldClass =
  "mt-2 w-full rounded-xl border border-white/10 bg-black/25 px-4 py-3 text-white outline-none transition placeholder:text-white/25 focus:border-emerald-400/60 focus:ring-4 focus:ring-emerald-400/10";


export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [district, setDistrict] = useState("");
  const [userType, setUserType] = useState("household");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await registerUser({
        full_name: fullName,
        email,
        password,
        district: district || undefined,
        user_type: userType,
      });
      router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell
      eyebrow="Join HelioSL"
      title="Create your energy profile"
      description="A few details help HelioSL tailor your dashboard and future guidance."
      footer={
        <>
          Already have an account?{" "}
          <Link href="/login" className="font-semibold text-emerald-300 hover:text-emerald-200">
            Sign in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label htmlFor="full-name" className="text-sm font-medium text-white/75">Full name</label>
            <input id="full-name" value={fullName} onChange={(event) => setFullName(event.target.value)} required autoComplete="name" placeholder="Your name" className={fieldClass} />
          </div>

          <div className="sm:col-span-2">
            <label htmlFor="email" className="text-sm font-medium text-white/75">Email address</label>
            <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required autoComplete="email" placeholder="you@example.com" className={fieldClass} />
          </div>

          <div>
            <label htmlFor="district" className="text-sm font-medium text-white/75">District</label>
            <input id="district" value={district} onChange={(event) => setDistrict(event.target.value)} placeholder="e.g. Colombo" className={fieldClass} />
          </div>

          <div>
            <label htmlFor="user-type" className="text-sm font-medium text-white/75">Profile type</label>
            <select id="user-type" value={userType} onChange={(event) => setUserType(event.target.value)} className={fieldClass}>
              <option value="household">Household</option>
              <option value="business">Business</option>
            </select>
          </div>

          <div className="sm:col-span-2">
            <div className="flex items-center justify-between gap-3">
              <label htmlFor="password" className="text-sm font-medium text-white/75">Password</label>
              <button type="button" onClick={() => setShowPassword((current) => !current)} className="text-xs font-medium text-emerald-300 hover:text-emerald-200">
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
            <input id="password" type={showPassword ? "text" : "password"} value={password} onChange={(event) => setPassword(event.target.value)} required minLength={8} autoComplete="new-password" placeholder="At least 8 characters" className={fieldClass} />
          </div>
        </div>

        {error && (
          <p role="alert" className="rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-200">{error}</p>
        )}

        <button type="submit" disabled={loading} className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-400 px-4 py-3.5 font-semibold text-[#06110d] transition hover:bg-emerald-300 disabled:cursor-wait disabled:opacity-60">
          {loading && <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#06110d]/25 border-t-[#06110d]" />}
          {loading ? "Creating your profile..." : "Create my HelioSL account"}
        </button>

        <p className="text-center text-xs leading-5 text-white/35">
          Your energy records remain scoped to your authenticated account.
        </p>
      </form>
    </AuthShell>
  );
}
