"use client";

import { useRouter } from "next/navigation";

import { removeToken } from "@/lib/auth";


export function Sidebar() {
  const router = useRouter();

  function logout() {
    removeToken();

    router.push("/login");
  }

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-neutral-800 bg-neutral-950 p-6">
      <div>
        <p className="text-sm text-emerald-400">
          HelioSL
        </p>

        <h2 className="mt-1 text-xl font-semibold text-white">
          Energy Intelligence
        </h2>
      </div>

      <nav className="mt-10 space-y-3 text-sm">
        <a
          href="/dashboard"
          className="block rounded-lg bg-neutral-800 px-4 py-3 text-white"
        >
          Overview
        </a>

        <a
          href="#"
          className="block px-4 py-3 text-neutral-400"
        >
          Energy
        </a>

        <a
          href="#"
          className="block px-4 py-3 text-neutral-400"
        >
          Solar
        </a>

        <a
          href="#"
          className="block px-4 py-3 text-neutral-400"
        >
          AI Assistant
        </a>
      </nav>

      <button
        onClick={logout}
        className="mt-auto rounded-lg border border-neutral-700 px-4 py-3 text-sm text-neutral-300"
      >
        Log out
      </button>
    </aside>
  );
}