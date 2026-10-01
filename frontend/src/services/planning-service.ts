import { apiRequest } from "@/lib/api";

import type {
  PlanningRequest,
  PlanningScenario,
} from "@/types/planning";


export function calculateScenario(
  data: PlanningRequest
) {
  return apiRequest<PlanningScenario>(
    "/planning/scenario",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}