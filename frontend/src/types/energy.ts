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