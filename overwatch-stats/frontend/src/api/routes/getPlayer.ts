import type { PlayerProfile, PlayerProfileSummary } from "../../../types";
import { apiClient } from "../apiClient";

export async function getPlayer(userTag: string): Promise<PlayerProfile> {
  return apiClient<PlayerProfile>(`/players/${encodeURIComponent(userTag)}`);
}

export async function getAllPlayer(): Promise<PlayerProfileSummary[]> {
  return apiClient<PlayerProfileSummary[]>("/players/comparison-list");
}
