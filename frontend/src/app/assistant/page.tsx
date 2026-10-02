"use client";

import {
  FormEvent,
  useState,
} from "react";

import {
  AgentFlow,
} from "@/components/assistant/agent-flow";
import {
  FormattedAssistantMessage,
} from "@/components/assistant/formatted-assistant-message";
import {
  TransparencyPanel,
} from "@/components/assistant/transparency-panel";
import type {
  AgentStage,
} from "@/components/assistant/agent-flow";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import {
  streamAssistantMessage,
} from "@/services/assistant-service";
import type {
  AgenticAssistantResponse,
} from "@/types/assistant";


interface Message {
  role: "user" | "assistant";
  content: string;
  transparency?: AgenticAssistantResponse;
}


function initialAgentStages(): AgentStage[] {
  return [
    { id: "nlp", label: "Query Analysis", status: "waiting" },
    { id: "orchestrator", label: "Orchestrator", status: "waiting" },
    { id: "energy", label: "Energy Intelligence", status: "waiting" },
    { id: "weather", label: "Weather Intelligence", status: "waiting" },
    { id: "knowledge", label: "Knowledge Retrieval", status: "waiting" },
    { id: "financial", label: "Financial Planning", status: "waiting" },
    { id: "generate", label: "Response Synthesis", status: "waiting" },
    { id: "safety", label: "Safety Verification", status: "waiting" },
  ];
}


export default function AssistantPage() {
  const [input, setInput] =
    useState("");

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [stages, setStages] =
    useState<AgentStage[]>([]);


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setError("");
    setStages(initialAgentStages());
    setLoading(true);

    try {
      const response =
        await streamAssistantMessage(
          message,
          (stage) => {
            setStages((current) =>
              current.map((item) =>
                item.id === stage.agent
                  ? {
                      ...item,
                      label: stage.label,
                      status: stage.status,
                    }
                  : item
              )
            );
          }
        );

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.message,
          transparency: response,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "HelioSL AI request failed"
      );
    } finally {
      setLoading(false);
    }
  }


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
            Agent-orchestrated energy intelligence,
            trusted retrieval, and safety review.
          </p>
        </div>

        <div className="mt-8 flex-1 overflow-y-auto rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center">
              <div className="max-w-lg text-center">
                <h2 className="text-xl font-medium text-white">
                  Ask HelioSL
                </h2>

                <p className="mt-3 text-sm text-neutral-400">
                  Try asking about solar generation,
                  electricity consumption, solar capacity,
                  or renewable energy concepts.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-5">
              {messages.map(
                (message, index) => (
                  <div
                    key={index}
                    className={
                      message.role === "user"
                        ? "ml-auto max-w-2xl rounded-2xl bg-emerald-500 p-4 text-black"
                        : "max-w-2xl rounded-2xl bg-neutral-800 p-4 text-neutral-100"
                    }
                  >
                    {message.role === "assistant" ? (
                      <FormattedAssistantMessage
                        content={message.content}
                      />
                    ) : (
                      <p className="whitespace-pre-wrap">
                        {message.content}
                      </p>
                    )}

                    {message.role === "assistant" &&
                      message.transparency && (
                        <TransparencyPanel
                          response={message.transparency}
                        />
                      )}
                  </div>
                )
              )}

              {stages.length > 0 && (
                <AgentFlow stages={stages} />
              )}
            </div>
          )}
        </div>

        {error && (
          <p className="mt-3 text-sm text-red-400">
            {error}
          </p>
        )}

        <form
          onSubmit={handleSubmit}
          className="mt-5 flex gap-3"
        >
          <input
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            placeholder="Ask HelioSL..."
            className="flex-1 rounded-xl border border-neutral-700 bg-neutral-900 px-5 py-4 text-white"
          />

          <button
            type="submit"
            disabled={loading}
            className="rounded-xl bg-emerald-500 px-6 font-medium text-black disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </div>
    </DashboardShell>
  );
}
