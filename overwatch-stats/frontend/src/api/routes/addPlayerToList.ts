import type { PlayerProfile } from "../../../types";
import { apiClient } from "../apiClient";

export async function addPlayerToList(profile: PlayerProfile) : Promise<PlayerProfile>{
return apiClient<PlayerProfile>(`/players/add-comparison-list`, {
		method: 'POST',
		body: JSON.stringify(profile),
		headers: {
			'Content-Type': 'application/json',
		},
	});
}

