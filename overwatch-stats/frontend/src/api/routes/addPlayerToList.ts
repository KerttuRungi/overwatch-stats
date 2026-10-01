import type { PlayerProfileSummary } from "../../../types";
import { apiClient } from "../apiClient";

export async function addPlayerToList(
  profile: PlayerProfileSummary,
): Promise<PlayerProfileSummary> {
  return apiClient<PlayerProfileSummary>(`/players/add-comparison-list`, {
    method: "POST",
    body: JSON.stringify(profile),
    headers: {
      "Content-Type": "application/json",
    },
  });
}
