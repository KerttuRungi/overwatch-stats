import type { PlayerProfileSummary } from "../../../types";
import { apiClient } from "../apiClient";

export async function removePlayerFromList(
  username: string,
): Promise<PlayerProfileSummary> {
  return apiClient<PlayerProfileSummary>(
    `/players/comparison-list/${encodeURIComponent(username)}`,
    {
      method: "DELETE",
    },
  );
}
