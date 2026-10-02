export interface AgenticAssistantResponse {
  message: string;
  intent: string;
  entities: Record<string, unknown>;
  normalized_query: string;
  selected_agents: string[];
  energy_result?: Record<string, unknown> | null;
  weather_result?: Record<string, unknown> | null;
  knowledge_result?: Record<string, unknown> | null;
  financial_result?: Record<string, unknown> | null;
  sources: {
    number?: number;
    document_id?: number;
    title?: string;
    organization?: string | null;
    published_year?: number | null;
    effective_date?: string | null;
    document_type?: string | null;
    authority_level?: number | null;
    source_url?: string | null;
  }[];
  confidence: "high" | "medium" | "low";
  safety_passed: boolean;
  safety_notes: string[];
  trace: string[];
}

export type AgentStageStatus =
  | "waiting"
  | "running"
  | "complete"
  | "skipped"
  | "error";

export interface AssistantStageEvent {
  agent: string;
  label: string;
  status: AgentStageStatus;
}

export interface AssistantFinalEvent {
  answer: string;
  sources: AgenticAssistantResponse["sources"];
  response: AgenticAssistantResponse;
}
