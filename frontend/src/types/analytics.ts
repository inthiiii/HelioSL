export interface EnergyIntelligenceSummary {
  average_consumption_kwh: number | null;
  latest_consumption_kwh: number | null;
  consumption_change_percent: number | null;

  average_generation_kwh: number | null;
  latest_generation_kwh: number | null;
  generation_change_percent: number | null;

  consumption_trend: string;
  generation_trend: string;

  generation_anomaly: boolean;
}