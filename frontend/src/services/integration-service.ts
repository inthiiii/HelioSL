import { apiRequest } from "@/lib/api";

import type {
  IntegratedSummary,
} from "@/types/integration";


export function getIntegratedSummary() {
  return apiRequest<IntegratedSummary>(
    "/integration/summary"
  );
}
