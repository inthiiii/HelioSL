"use client";

import { useState } from "react";

import { DashboardShell } from "@/components/layout/dashboard-shell";


export default function AssistantPage() {
  const [message, setMessage] = useState("");


  return (
    <DashboardShell>
      <div className="flex h-[calc(100vh-5rem)] flex-col">
        <div>
          <p className="text-sm text-neutral-400">
            HelioSL AI
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            Renewable Energy Assistant
          </h1>

          <p className="mt-2 text-neutral-400">
            Ask questions about your energy usage,
            solar system, and renewable energy.
          </p>
        </div>

        <div className="mt-8 flex-1 rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          <div className="flex h-full items-center justify-center">
            <div className="max-w-md text-center">
              <p className="text-lg font-medium text-white">
                HelioSL Intelligence
              </p>

              <p className="mt-2 text-sm text-neutral-400">
                LLM, retrieval and multi-agent intelligence
                will be connected in the upcoming phases.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-5 flex gap-3">
          <input
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            placeholder="Ask HelioSL..."
            disabled
            className="flex-1 rounded-xl border border-neutral-700 bg-neutral-900 px-5 py-4 text-white disabled:opacity-60"
          />

          <button
            disabled
            className="rounded-xl bg-emerald-500 px-6 font-medium text-black disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </DashboardShell>
  );
}