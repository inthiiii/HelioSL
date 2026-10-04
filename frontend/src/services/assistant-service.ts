import { API_BASE_URL, apiRequest } from "@/lib/api";
import { getToken } from "@/lib/auth";

import type {
  AgenticAssistantResponse,
  AssistantFinalEvent,
  AssistantStageEvent,
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


export async function streamAssistantMessage(
  message: string,
  onStage: (stage: AssistantStageEvent) => void
): Promise<AgenticAssistantResponse> {
  const token = getToken();

  const response = await fetch(
    `${API_BASE_URL}/assistant/agentic/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token
          ? { Authorization: `Bearer ${token}` }
          : {}),
      },
      body: JSON.stringify({ message }),
    }
  );

  if (!response.ok) {
    let message = `HelioSL AI request failed (${response.status})`;

    try {
      const data = await response.json() as {
        detail?: string;
      };

      if (data.detail) {
        message = data.detail;
      }
    } catch {
      // Keep the status-based fallback when no JSON body is available.
    }

    throw new Error(message);
  }

  if (!response.body) {
    throw new Error("Streaming is unavailable");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalResponse: AgenticAssistantResponse | null = null;

  function processFrame(frame: string) {
    let eventName = "message";
    const dataLines: string[] = [];

    for (const line of frame.split("\n")) {
      if (line.startsWith("event:")) {
        eventName = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        dataLines.push(line.slice(5).trim());
      }
    }

    if (dataLines.length === 0) {
      return;
    }

    const data = JSON.parse(
      dataLines.join("\n")
    ) as Record<string, unknown>;

    if (eventName === "stage") {
      onStage(data as unknown as AssistantStageEvent);
      return;
    }

    if (eventName === "final") {
      finalResponse = (
        data as unknown as AssistantFinalEvent
      ).response;
      return;
    }

    if (eventName === "error") {
      const stage: AssistantStageEvent = {
        agent: String(data.agent ?? "synthesis"),
        status: "error",
        label: String(
          data.message ?? "Agentic workflow failed"
        ),
      };
      onStage(stage);
      throw new Error(stage.label);
    }
  }

  while (true) {
    const { value, done } = await reader.read();

    buffer += decoder
      .decode(value, { stream: !done })
      .replaceAll("\r", "");

    let boundary = buffer.indexOf("\n\n");

    while (boundary !== -1) {
      processFrame(buffer.slice(0, boundary));
      buffer = buffer.slice(boundary + 2);
      boundary = buffer.indexOf("\n\n");
    }

    if (done) {
      break;
    }
  }

  if (buffer.trim()) {
    processFrame(buffer.trim());
  }

  if (!finalResponse) {
    throw new Error(
      "The agentic stream ended without an answer"
    );
  }

  return finalResponse;
}
