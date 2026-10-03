import { apiRequest } from "@/lib/api";

import type {
  BillExtraction,
  ConsumptionCreate,
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


export function extractElectricityBill(
  file: File
) {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<BillExtraction>(
    "/energy/me/bills/extract",
    {
      method: "POST",
      body: formData,
    }
  );
}


export function createConsumptionRecord(
  data: ConsumptionCreate
) {
  return apiRequest<ConsumptionRecord>(
    "/energy/me/consumption",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}
