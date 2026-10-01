import { apiRequest } from "@/lib/api";

import type {
  AgenticAssistantResponse,
} from "@/types/assistant";


export function sendAssistantMessage(
  message: string
) {
  return apiRequest<AgenticAssistantResponse>(
    "/assistant/agentic",
    {
      method: "POST",
      body: JSON.stringify({
        message,
      }),
    }
  );
}
