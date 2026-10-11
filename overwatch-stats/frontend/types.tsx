
export type PlayerProfile = {
	summary: {
		username: string
		avatar: string
		namecard: string
	}
}
export type PlayerProfileSummary = {
	username: string
	avatar: string
	namecard: string
}
export type GeneralStats = {
	games_played: number
	games_won: number
	games_lost: number
	time_played: number
	winrate: number
}
export type HeroStats = {
	hero: string
	games_played: number
	games_won: number
	time_played: number
	winrate: number
}
export type PlayerStatsComparison = {
	username: string
	avatar: string
	general: GeneralStats | null
	top_heroes: HeroStats[]
	error: string | null
}
export type StatsComparisonResponse = {
	players: PlayerStatsComparison[]
	most_wins: string[]
}
export type PlayerRoleProfile = {
	username: string
	avatar: string
	main_role: string | null
	role_hours: Record<string, number>
	top_heroes: HeroStats[]
	error: string | null
}
export type RoleAssignment = {
	username: string
	assigned_role: string
	main_role: string
	fit: number
}
export type RoleSuggestion = {
	username: string
	from_role: string
	to_role: string
	fit: number
	message: string
}
export type TeamCompatibilityResponse = {
	players: PlayerRoleProfile[]
	assignments: RoleAssignment[]
	open_slots: string[]
	substitutes: string[]
	score: number
	compatible: boolean
	warnings: string[]
	suggestions: RoleSuggestion[]
}
