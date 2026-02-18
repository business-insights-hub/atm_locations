export type LocationRecord = {
  source: string;
  type: string;
  location_id: string;
  name: string;
  address: string;
  city: string;
  country: string;
  latitude: number;
  longitude: number;
  phone: string;
  email: string;
  website: string;
  working_hours_weekday: string;
  working_hours_saturday: string;
  working_hours_sunday: string;
  cash_in: string;
  nfc: string;
  twentyFourSeven: string;
  work_on_weekend: string;
  additional_info: string;
};

export type CoverageGap = {
  latitude: number;
  longitude: number;
  source: string;
  address: string;
  distance_to_bob: number;
  competitor_density: number;
  roi_score?: number;
};

export type RetailOpportunity = {
  source: string;
  address: string;
  latitude: number;
  longitude: number;
  distance_to_bob: number;
  competitor_density: number;
  opportunity_score: number;
};

export type DashboardMetrics = {
  bobAtmCount: number;
  totalAtmCount: number;
  marketSharePct: number;
  leaderName: string;
  leaderCount: number;
  gapToLeader: number;
};
