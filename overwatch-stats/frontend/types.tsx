
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
