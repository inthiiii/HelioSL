"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

import { AgentFlow } from "@/components/assistant/agent-flow";
import type { AgentStage } from "@/components/assistant/agent-flow";
import { FormattedAssistantMessage } from "@/components/assistant/formatted-assistant-message";
import { TransparencyPanel } from "@/components/assistant/transparency-panel";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { streamAssistantMessage } from "@/services/assistant-service";
import type { AgenticAssistantResponse } from "@/types/assistant";


interface ChatTurn {
  id: number;
  question: string;
  answer: string | null;
  failed?: boolean;
  transparency?: AgenticAssistantResponse;
}


const openingSuggestions = [
  "Why is my electricity usage increasing?",
  "Why has my solar generation decreased?",
  "What does my recent energy trend show?",
  "What information is needed to plan a solar system?",
];


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


function followUpQuestions(response: AgenticAssistantResponse | null): string[] {
  if (!response) return openingSuggestions;

  if (response.intent === "solar_performance") {
    return [
      "How does this compare with my previous months?",
      "What safe checks should I make next?",
      "Could weather have contributed to this change?",
    ];
  }

  if (response.intent === "energy_usage") {
    return [
      "Which month changed the most?",
      "What information could explain this increase?",
      "How does my usage compare with my recorded average?",
    ];
  }

  if (["solar_planning", "financial"].includes(response.intent)) {
    return [
      "Which planning inputs are still missing?",
      "How does self-consumption affect the estimate?",
      "Show me a conservative planning approach.",
    ];
  }

  return [
    "Can you explain that more simply?",
    "Which trusted sources support this?",
    "What should I consider next?",
  ];
}


export default function AssistantPage() {
  const [input, setInput] = useState("");
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [loading, setLoading] = useState(false);
  const [stages, setStages] = useState<AgentStage[]>(initialAgentStages());
  const [activeResponse, setActiveResponse] = useState<AgenticAssistantResponse | null>(null);
  const flowRef = useRef<HTMLDivElement | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const turnCounterRef = useRef(0);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [turns, loading]);

  useEffect(() => {
    if (!loading) return;
    flowRef.current?.focus({ preventScroll: true });
    flowRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [loading]);

  async function submitMessage(message: string) {
    const cleanMessage = message.trim();
    if (!cleanMessage || loading) return;

    turnCounterRef.current += 1;
    const turnId = turnCounterRef.current;

    setTurns((current) => [
      ...current,
      {
        id: turnId,
        question: cleanMessage,
        answer: null,
      },
    ]);
    setInput("");
    setActiveResponse(null);
    setStages(initialAgentStages());
    setLoading(true);

    try {
      const response = await streamAssistantMessage(cleanMessage, (stage) => {
        setStages((current) => current.map((item) =>
          item.id === stage.agent
            ? { ...item, label: stage.label, status: stage.status }
            : item
        ));
      });

      setTurns((current) => current.map((turn) =>
        turn.id === turnId
          ? {
              ...turn,
              answer: response.message,
              transparency: response,
            }
          : turn
      ));
      setActiveResponse(response);
    } catch (requestError) {
      const message = requestError instanceof Error
        ? requestError.message
        : "HelioSL AI could not complete this request.";

      setTurns((current) => current.map((turn) =>
        turn.id === turnId
          ? {
              ...turn,
              answer: message,
              failed: true,
            }
          : turn
      ));
      setStages((current) => current.map((stage, index) =>
        index === 0
          ? {
              ...stage,
              label: "Request safely stopped",
              status: "error",
            }
          : stage.status === "waiting"
            ? { ...stage, status: "skipped" }
            : stage
      ));
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void submitMessage(input);
  }

  const suggestions = followUpQuestions(activeResponse);

  return (
    <DashboardShell>
      <div className="flex min-h-[calc(100vh-8rem)] flex-col">
        <div>
          <p className="text-sm text-neutral-400">HelioSL AI</p>
          <h1 className="mt-2 text-3xl font-semibold text-white">Renewable Energy Assistant</h1>
          <p className="mt-2 text-neutral-400">Ask naturally. See how each specialist contributes to a responsible answer.</p>
        </div>

        <div className="mt-7 grid min-h-0 flex-1 gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
          <section className="flex h-[calc(100vh-11rem)] min-h-[620px] max-h-[900px] min-w-0 flex-col overflow-hidden rounded-2xl border border-neutral-800 bg-neutral-900">
            <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-4 sm:p-6">
              {turns.length === 0 ? (
                <div className="flex min-h-full items-center justify-center py-12">
                  <div className="max-w-xl text-center">
                    <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl border border-emerald-400/20 bg-emerald-400/10 text-2xl text-emerald-300">✦</span>
                    <h2 className="mt-5 text-2xl font-semibold text-white">How can HelioSL help today?</h2>
                    <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-neutral-400">
                      Ask about your electricity use, solar performance, planning inputs or trusted renewable-energy knowledge.
                    </p>
                    <div className="mt-7 grid gap-2 sm:grid-cols-2">
                      {openingSuggestions.map((suggestion) => (
                        <button
                          key={suggestion}
                          type="button"
                          onClick={() => void submitMessage(suggestion)}
                          className="rounded-xl border border-neutral-700 bg-neutral-950/55 p-3 text-left text-sm text-neutral-300 transition hover:border-emerald-400/35 hover:text-white"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="mx-auto max-w-3xl space-y-5">
                  {turns.map((turn) => (
                    <div key={turn.id} className="space-y-3 border-b border-neutral-800/70 pb-5 last:border-0">
                      <div className="ml-auto max-w-[85%] rounded-2xl rounded-br-md bg-emerald-400 p-4 text-[#06110d]">
                        <p className="whitespace-pre-wrap">{turn.question}</p>
                      </div>

                      {turn.answer && (
                        <div className={`mr-auto max-w-[92%] rounded-2xl rounded-bl-md border p-5 text-neutral-100 ${
                          turn.failed
                            ? "border-amber-500/25 bg-amber-500/[0.07]"
                            : "border-neutral-700/70 bg-neutral-800"
                        }`}>
                          {turn.failed && (
                            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-amber-300">
                              Request not processed
                            </p>
                          )}
                          <FormattedAssistantMessage content={turn.answer} />
                        </div>
                      )}
                    </div>
                  ))}

                  {loading && (
                    <div className="mr-auto flex items-center gap-3 rounded-2xl rounded-bl-md border border-emerald-400/20 bg-emerald-400/[0.06] px-4 py-3 text-sm text-emerald-200">
                      <span className="flex gap-1">
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-emerald-300 [animation-delay:-0.2s]" />
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-emerald-300 [animation-delay:-0.1s]" />
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-emerald-300" />
                      </span>
                      Specialists are building your answer
                    </div>
                  )}

                  {!loading && activeResponse && (
                    <div className="pt-2">
                      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-neutral-500">Suggested follow-up questions</p>
                      <div className="flex flex-wrap gap-2">
                        {suggestions.map((suggestion) => (
                          <button
                            key={suggestion}
                            type="button"
                            onClick={() => void submitMessage(suggestion)}
                            className="rounded-full border border-neutral-700 bg-neutral-950/50 px-3.5 py-2 text-xs text-neutral-300 transition hover:border-emerald-400/40 hover:text-emerald-300"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            <form onSubmit={handleSubmit} className="border-t border-neutral-800 bg-neutral-950/45 p-3 sm:p-4">
              <div className="mx-auto flex max-w-3xl gap-3">
                <input
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  placeholder="Ask HelioSL about your energy..."
                  aria-label="Message HelioSL"
                  className="min-w-0 flex-1 rounded-xl border border-neutral-700 bg-neutral-950 px-4 py-3.5 text-white outline-none transition placeholder:text-neutral-600 focus:border-emerald-400/50"
                />
                <button type="submit" disabled={loading || !input.trim()} className="rounded-xl bg-emerald-400 px-5 font-semibold text-neutral-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-40">
                  Send
                </button>
              </div>
            </form>
          </section>

          <aside
            ref={flowRef}
            tabIndex={-1}
            aria-live="polite"
            className={`h-[calc(100vh-11rem)] min-h-[620px] max-h-[900px] min-w-0 overflow-y-auto overscroll-contain rounded-2xl border bg-neutral-900 p-4 outline-none transition-all sm:p-5 ${
              loading
                ? "border-emerald-400/45 shadow-[0_0_45px_rgba(52,211,153,0.10)] ring-2 ring-emerald-400/15"
                : "border-neutral-800"
            }`}
          >
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-300">Intelligence panel</p>
                <h2 className="mt-1 font-semibold text-white">How your answer is built</h2>
              </div>
              {loading && <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-400" />}
            </div>

            <AgentFlow stages={stages} />

            {activeResponse ? (
              <TransparencyPanel response={activeResponse} />
            ) : (
              <div className="mt-5 rounded-xl border border-dashed border-neutral-700 p-4 text-xs leading-5 text-neutral-500">
                Sources, agents used, safety notes, confidence and execution traces will appear here with the completed answer.
              </div>
            )}
          </aside>
        </div>
      </div>
    </DashboardShell>
  );
}
