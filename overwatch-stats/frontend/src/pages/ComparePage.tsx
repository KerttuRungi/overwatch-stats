import { useEffect, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import type {
  GeneralStats,
  PlayerStatsComparison,
  StatsComparisonResponse,
} from "../../types";
import { getComparisonStats } from "../api/routes/getComparisonStats";

type StatRow = {
  label: string;
  render: (general: GeneralStats) => ReactNode;
};

const statRows: StatRow[] = [
  { label: "Games won", render: (general) => general.games_won },
  { label: "Games lost", render: (general) => general.games_lost },
  { label: "Games played", render: (general) => general.games_played },
  { label: "Winrate", render: (general) => `${general.winrate.toFixed(1)}%` },
  { label: "Time played", render: (general) => formatHours(general.time_played) },
];

function formatHours(seconds: number) {
  return `${Math.round(seconds / 3600)} h`;
}

function formatHeroName(hero: string) {
  return hero
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function ComparePage() {
  const [comparison, setComparison] = useState<StatsComparisonResponse | null>(
    null,
  );
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;

    getComparisonStats()
      .then((data) => {
        if (!ignore) setComparison(data);
      })
      .catch((requestError) => {
        if (!ignore) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : "Unable to load stats",
          );
        }
      })
      .finally(() => {
        if (!ignore) setIsLoading(false);
      });

    return () => {
      ignore = true;
    };
  }, []);

  const players = comparison?.players ?? [];
  const mostWins = new Set(comparison?.most_wins ?? []);

  function cellClass(player: PlayerStatsComparison) {
    return mostWins.has(player.username) ? "stat-leader" : undefined;
  }

  return (
    <main className="app-shell">
      <header className="page-header">
        <Link to="/" className="back-link">
          ← Back
        </Link>
        <p className="intro">Stat comparison of players in your list.</p>
      </header>

      {isLoading && <p>Loading stats...</p>}
      {error && <p className="status-message error-message">{error}</p>}
      {!isLoading && !error && players.length === 0 && (
        <p>No players in the list yet.</p>
      )}

      {players.length > 0 && (
        <div className="compare-table-wrapper">
          <table className="compare-table">
            <thead>
              <tr>
                <th scope="col" />
                {players.map((player) => (
                  <th
                    key={player.username}
                    scope="col"
                    className={cellClass(player)}
                  >
                    <img
                      className="compare-avatar"
                      src={player.avatar}
                      alt={`${player.username} avatar`}
                    />
                    <div>{player.username}</div>
                    {mostWins.has(player.username) && (
                      <span className="leader-badge">Most wins</span>
                    )}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {statRows.map((row) => (
                <tr key={row.label}>
                  <th scope="row">{row.label}</th>
                  {players.map((player) => (
                    <td key={player.username} className={cellClass(player)}>
                      {player.general ? row.render(player.general) : "–"}
                    </td>
                  ))}
                </tr>
              ))}
              <tr>
                <th scope="row">Top 3 heroes</th>
                {players.map((player) => (
                  <td key={player.username} className={cellClass(player)}>
                    {player.error ? (
                      <span className="error-message">{player.error}</span>
                    ) : (
                      <ol className="hero-list">
                        {player.top_heroes.map((hero) => (
                          <li key={hero.hero}>
                            {formatHeroName(hero.hero)}{" "}
                            <small>
                              {formatHours(hero.time_played)} ·{" "}
                              {hero.winrate.toFixed(1)}%
                            </small>
                          </li>
                        ))}
                      </ol>
                    )}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
