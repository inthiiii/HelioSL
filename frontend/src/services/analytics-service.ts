import { apiRequest } from "@/lib/api";

import type {
  EnergyIntelligenceSummary,
} from "@/types/analytics";


export function getEnergyIntelligenceSummary() {
  return apiRequest<EnergyIntelligenceSummary>(
    "/analytics/summary"
  );
}