export interface AgenticAssistantResponse {
  message: string;
  intent: string;
  entities: Record<string, unknown>;
  normalized_query: string;
  selected_agents: string[];
  energy_result?: Record<string, unknown> | null;
  knowledge_result?: Record<string, unknown> | null;
  financial_result?: Record<string, unknown> | null;
  sources: {
    number?: number;
    document_id?: number;
    title?: string;
    organization?: string | null;
    source_url?: string | null;
  }[];
  safety_passed: boolean;
  safety_notes: string[];
  trace: string[];
}
