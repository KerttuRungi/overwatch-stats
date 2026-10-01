import { useMemo } from "react";
import "./App.css";
import Search from "./components/Search";
import PlayerList from "./components/PlayerList";
import { usePlayerList } from "./hooks/usePlayerList";

function App() {
  const { players, error, isLoading, reload } = usePlayerList();
  const listedUsernames = useMemo(
    () => new Set(players.map((player) => player.username)),
    [players],
  );

  return (
    <main className="app-shell">
      <header className="page-header">
        <p className="intro">
          Search a BattleTag to pull up a player profile from Overfast.
        </p>
      </header>
      <Search listedUsernames={listedUsernames} onListChanged={reload} />
      <PlayerList
        players={players}
        isLoading={isLoading}
        error={error}
        onListChanged={reload}
      />
      <button className="justify-center items-center">compare stats</button>
    </main>
  );
}

export default App;
