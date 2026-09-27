export interface AssistantResponse {
  message: string;
  intent: string;
  entities: Record<string, unknown>;
  normalized_query: string;
  provider: string;
  model: string;
  disclaimer: string;
}