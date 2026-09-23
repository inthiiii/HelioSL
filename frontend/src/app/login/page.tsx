"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

import { removeToken, saveToken } from "@/lib/auth";
import {
  getCurrentUser,
  loginUser,
} from "@/services/auth-service";


export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await loginUser({
        email,
        password,
      });

      saveToken(response.access_token);

      const currentUser = await getCurrentUser();

      setSuccess(
        `Welcome back, ${currentUser.full_name}. You are signed in.`
      );
      setPassword("");
    } catch (err) {
      removeToken();

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Login failed");
      }
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="min-h-screen flex items-center justify-center bg-neutral-950 px-6">
      <div className="w-full max-w-md rounded-2xl border border-neutral-800 bg-neutral-900 p-8">
        <div className="mb-8">
          <p className="text-sm text-emerald-400">
            HelioSL
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            Welcome back
          </h1>

          <p className="mt-2 text-sm text-neutral-400">
            Sign in to your renewable energy dashboard.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >
          <div>
            <label
              htmlFor="email"
              className="text-sm text-neutral-300"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="text-sm text-neutral-300"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          {error && (
            <p role="alert" className="text-sm text-red-400">
              {error}
            </p>
          )}

          {success && (
            <p role="status" className="text-sm text-emerald-400">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-emerald-500 px-4 py-3 font-medium text-black disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-neutral-400">
          New to HelioSL?{" "}
          <Link
            href="/register"
            className="font-medium text-emerald-400 hover:text-emerald-300"
          >
            Create an account
          </Link>
        </p>
      </div>
    </main>
  );
}
