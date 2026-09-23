"use client";

import { FormEvent, useState } from "react";

import { registerUser } from "@/services/auth-service";


export default function RegisterPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [district, setDistrict] = useState("");
  const [userType, setUserType] = useState("household");

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
      await registerUser({
        full_name: fullName,
        email,
        password,
        district: district || undefined,
        user_type: userType,
      });

      setSuccess("Account created successfully.");
      setFullName("");
      setEmail("");
      setPassword("");
      setDistrict("");
      setUserType("household");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Registration failed");
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
            Create your account
          </h1>

          <p className="mt-2 text-sm text-neutral-400">
            Start building your renewable energy profile.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >
          <div>
            <label className="text-sm text-neutral-300">
              Full name
            </label>

            <input
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-neutral-300">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-neutral-300">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-neutral-300">
              District
            </label>

            <input
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-neutral-300">
              User type
            </label>

            <select
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
              className="mt-2 w-full rounded-lg border border-neutral-700 bg-neutral-950 px-4 py-3 text-white"
            >
              <option value="household">
                Household
              </option>

              <option value="business">
                Business
              </option>
            </select>
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
            {loading
              ? "Creating account..."
              : "Create account"}
          </button>
        </form>
      </div>
    </main>
  );
}
