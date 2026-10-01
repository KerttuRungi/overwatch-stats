import type { StatsComparisonResponse } from "../../../types";
import { apiClient } from "../apiClient";

export async function getComparisonStats(): Promise<StatsComparisonResponse> {
  return apiClient<StatsComparisonResponse>("/players/comparison-list/stats");
}
