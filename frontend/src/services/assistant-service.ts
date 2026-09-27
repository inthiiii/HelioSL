import { apiRequest } from "@/lib/api";

import type {
  AssistantResponse,
} from "@/types/assistant";


export function sendAssistantMessage(
  message: string
) {
  return apiRequest<AssistantResponse>(
    "/assistant/analyze",
    {
      method: "POST",
      body: JSON.stringify({
        message,
      }),
    }
  );
}