import type { TeamCompatibilityResponse } from "../../../types";
import { apiClient } from "../apiClient";

export async function getTeamCompatibility(): Promise<TeamCompatibilityResponse> {
  return apiClient<TeamCompatibilityResponse>(
    "/players/comparison-list/team-compatibility",
  );
}
