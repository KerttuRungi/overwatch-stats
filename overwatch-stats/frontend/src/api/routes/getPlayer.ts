import type { PlayerProfile } from "../../../types";
import { apiClient } from "../apiClient";

export async function getPlayer(userTag: string) : Promise<PlayerProfile>{
return apiClient<PlayerProfile>(`/players/${encodeURIComponent(userTag)}`);
}

