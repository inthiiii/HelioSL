export interface PlanningRequest {
  average_monthly_consumption_kwh?: number;
  system_capacity_kw: number;
  installation_cost_lkr?: number;
  import_tariff_lkr_per_kwh?: number;
  export_rate_lkr_per_kwh?: number;
  specific_yield_kwh_per_kw_year?: number;
  self_consumption_ratio: number;
}


export interface PlanningScenario {
  system_capacity_kw: number;

  annual_consumption_kwh:
    | number
    | null;

  estimated_annual_generation_kwh:
    | number
    | null;

  self_consumed_solar_kwh:
    | number
    | null;

  exported_solar_kwh:
    | number
    | null;

  grid_import_kwh:
    | number
    | null;

  energy_coverage_percent:
    | number
    | null;

  avoided_import_cost_lkr:
    | number
    | null;

  export_income_lkr:
    | number
    | null;

  estimated_annual_benefit_lkr:
    | number
    | null;

  simple_payback_years:
    | number
    | null;

  calculation_ready: boolean;

  financial_calculation_ready: boolean;

  missing_inputs: string[];

  assumptions: string[];
}
