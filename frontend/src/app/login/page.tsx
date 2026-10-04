"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { AuthShell } from "@/components/auth/auth-shell";
import { removeToken, saveToken } from "@/lib/auth";
import { loginUser } from "@/services/auth-service";


const fieldClass =
  "mt-2 w-full rounded-xl border border-white/10 bg-black/25 px-4 py-3.5 text-white outline-none transition placeholder:text-white/25 focus:border-emerald-400/60 focus:ring-4 focus:ring-emerald-400/10";


export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await loginUser({ email, password });
      saveToken(response.access_token);
      router.replace("/dashboard");
    } catch (err) {
      removeToken();
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell
      eyebrow="Welcome back"
      title="Continue your energy journey"
      description="Sign in to see your latest energy, solar and AI-assisted insights."
      footer={
        <>
          New to HelioSL?{" "}
          <Link href="/register" className="font-semibold text-emerald-300 hover:text-emerald-200">
            Create an account
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="email" className="text-sm font-medium text-white/75">Email address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            autoComplete="email"
            placeholder="you@example.com"
            className={fieldClass}
          />
        </div>

        <div>
          <div className="flex items-center justify-between gap-3">
            <label htmlFor="password" className="text-sm font-medium text-white/75">Password</label>
            <button
              type="button"
              onClick={() => setShowPassword((current) => !current)}
              className="text-xs font-medium text-emerald-300 hover:text-emerald-200"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            autoComplete="current-password"
            placeholder="Enter your password"
            className={fieldClass}
          />
        </div>

        {error && (
          <p role="alert" className="rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-200">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-400 px-4 py-3.5 font-semibold text-[#06110d] shadow-[0_14px_35px_rgba(52,211,153,0.16)] transition hover:bg-emerald-300 disabled:cursor-wait disabled:opacity-60"
        >
          {loading && <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#06110d]/25 border-t-[#06110d]" />}
          {loading ? "Signing you in..." : "Sign in to HelioSL"}
        </button>
      </form>
    </AuthShell>
  );
}
