export interface SolarSystem {
  id: number;
  user_id: number;
  capacity_kw: string;
  installation_date?: string | null;
  scheme?: string | null;
  panel_brand?: string | null;
  inverter_brand?: string | null;
  installer_name?: string | null;
  created_at: string;
}

export interface SolarGenerationRecord {
  id: number;
  solar_system_id: number;
  generation_month: string;
  generation_kwh: string;
  exported_kwh?: string | null;
  imported_kwh?: string | null;
  created_at: string;
}