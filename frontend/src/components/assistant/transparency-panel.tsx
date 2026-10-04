import type {
  AgenticAssistantResponse,
} from "@/types/assistant";


interface TransparencyPanelProps {
  response: AgenticAssistantResponse;
}


const agentLabels: Record<string, string> = {
  energy: "Energy Intelligence",
  weather: "Weather Intelligence",
  knowledge: "Knowledge Retrieval",
  financial: "Financial Planning",
  safety: "Safety Verification",
};


const confidenceStyles = {
  high: "bg-emerald-500/15 text-emerald-300",
  medium: "bg-amber-500/15 text-amber-300",
  low: "bg-red-500/15 text-red-300",
};


export function TransparencyPanel({
  response,
}: TransparencyPanelProps) {
  const agents = Array.from(
    new Set([
      ...response.selected_agents,
      "safety",
    ])
  );

  return (
    <section className="mt-5 border-t border-neutral-700 pt-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-xs font-medium uppercase tracking-wide text-neutral-400">
          Responsible AI transparency
        </p>

        <span
          className={`rounded-full px-3 py-1 text-xs font-medium capitalize ${confidenceStyles[response.confidence]}`}
        >
          Confidence: {response.confidence}
        </span>
      </div>

      <div className="mt-4">
        <p className="text-xs font-medium text-neutral-300">
          Agents used
        </p>

        <div className="mt-2 flex flex-wrap gap-2">
          {agents.map((agent) => (
            <span
              key={agent}
              className="rounded-full border border-neutral-700 bg-neutral-900 px-3 py-1 text-xs text-neutral-300"
            >
              {agentLabels[agent] ?? agent}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-4">
        <p className="text-xs font-medium text-neutral-300">
          Trusted sources
        </p>

        {response.sources.length > 0 ? (
          <ul className="mt-2 space-y-2 text-sm">
            {response.sources.map((source, sourceIndex) => (
              <li key={source.document_id ?? sourceIndex}>
                {source.source_url ? (
                  <a
                    href={source.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-emerald-300 underline decoration-emerald-600 underline-offset-2"
                  >
                    {source.title ?? "Official source"}
                  </a>
                ) : (
                  <span>{source.title ?? "Official source"}</span>
                )}

                <span className="ml-2 text-xs text-neutral-400">
                  {[source.organization, source.published_year]
                    .filter(Boolean)
                    .join(" · ")}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-xs text-neutral-500">
            No trusted sources were attached to this answer.
          </p>
        )}
      </div>

      <div className="mt-4">
        <p className="text-xs font-medium text-neutral-300">
          Safety notes
        </p>

        {response.safety_notes.length > 0 ? (
          <ul className="mt-2 list-disc space-y-1 pl-5 text-xs text-amber-200">
            {response.safety_notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-xs text-emerald-300">
            Safety verification found no concerns.
          </p>
        )}
      </div>

      {response.trace.length > 0 && (
        <details className="mt-4 text-xs text-neutral-400">
          <summary className="cursor-pointer font-medium text-neutral-300">
            Execution trace
          </summary>

          <ol className="mt-2 list-decimal space-y-1 pl-5">
            {response.trace.map((item, index) => (
              <li key={`${index}-${item}`}>{item}</li>
            ))}
          </ol>
        </details>
      )}
    </section>
  );
}
