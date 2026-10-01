import type { PlayerProfileSummary } from "../../types";
import PlayerCard from "./PlayerCard";

type PlayerListProps = {
  players: PlayerProfileSummary[];
  isLoading: boolean;
  error: string;
  onListChanged: () => void;
};

export default function PlayerList({
  players,
  isLoading,
  error,
  onListChanged,
}: PlayerListProps) {
  return (
    <div>
      <h2>Players</h2>
      {isLoading && <p>Loading...</p>}
      {error && <p className="status-message error-message">{error}</p>}
      <ul>
        {players.map((player) => (
          <li key={player.username}>
            <PlayerCard
              profile={{ summary: player }}
              isInList
              onListChanged={onListChanged}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}
