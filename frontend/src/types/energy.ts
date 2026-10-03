export interface EnergyProfile {
  id: number;
  user_id: number;
  provider?: string | null;
  connection_type?: string | null;
  average_monthly_consumption_kwh?: string | null;
  average_monthly_bill_lkr?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ConsumptionRecord {
  id: number;
  user_id: number;
  billing_month: string;
  consumption_kwh: string;
  bill_amount_lkr?: string | null;
  created_at: string;
}

export interface BillExtraction {
  filename: string;
  provider: string | null;
  account_number: string | null;
  billing_month: string | null;
  consumption_kwh: string | null;
  bill_amount_lkr: string | null;
  previous_meter_reading: string | null;
  current_meter_reading: string | null;
  confidence: "high" | "medium" | "low";
  confidence_score: number;
  warnings: string[];
}

export interface ConsumptionCreate {
  billing_month: string;
  consumption_kwh: number;
  bill_amount_lkr?: number | null;
}
