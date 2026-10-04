import type {
  AgentStageStatus,
} from "@/types/assistant";


export interface AgentStage {
  id: string;
  label: string;
  status: AgentStageStatus;
}


interface AgentFlowProps {
  stages: AgentStage[];
}


const statusStyle: Record<AgentStageStatus, string> = {
  waiting: "border-neutral-700 bg-neutral-900 text-neutral-500",
  running: "border-amber-500/50 bg-amber-500/10 text-amber-300",
  complete: "border-emerald-500/40 bg-emerald-500/10 text-emerald-300",
  skipped: "border-neutral-800 bg-neutral-950 text-neutral-600",
  error: "border-red-500/50 bg-red-500/10 text-red-300",
};


const statusSymbol: Record<AgentStageStatus, string> = {
  waiting: "○",
  running: "●",
  complete: "✓",
  skipped: "—",
  error: "!",
};


export function AgentFlow({ stages }: AgentFlowProps) {
  return (
    <section className="rounded-xl border border-neutral-800 bg-neutral-950/70 p-4">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-medium text-white">
          Live agent flow
        </h2>

        <span className="text-[10px] uppercase tracking-wider text-neutral-600">Live</span>
      </div>

      <div className="space-y-2">
        {stages.map((stage) => (
          <div
            key={stage.id}
            className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-sm transition-colors ${statusStyle[stage.status]}`}
          >
            <span
              aria-hidden="true"
              className={
                stage.status === "running"
                  ? "animate-pulse"
                  : ""
              }
            >
              {statusSymbol[stage.status]}
            </span>

            <span>{stage.label}</span>

            <span className="ml-auto text-xs capitalize opacity-70">
              {stage.status}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
