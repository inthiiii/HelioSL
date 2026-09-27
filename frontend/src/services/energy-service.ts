import { apiRequest } from "@/lib/api";

import type {
  ConsumptionRecord,
  EnergyProfile,
} from "@/types/energy";


export function getEnergyProfile() {
  return apiRequest<EnergyProfile>(
    "/energy/me/profile"
  );
}


export function getConsumptionRecords() {
  return apiRequest<ConsumptionRecord[]>(
    "/energy/me/consumption"
  );
}