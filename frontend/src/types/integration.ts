export interface IntegratedSummary {
  user_type: string;
  district: string | null;

  energy_profile_available: boolean;
  solar_system_available: boolean;

  energy: Record<string, unknown>;
  solar: Record<string, unknown>;

  alerts: string[];
}
