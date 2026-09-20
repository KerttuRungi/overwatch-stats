import { useState, type SubmitEvent } from "react";
import type { PlayerProfile } from "../../types";
import { getPlayer } from "../api/routes/getPlayer";
import PLayerCard from "./PlayerCard";

const battleTagPattern = /^[^-]+-\d{4}$/;

function Search() {
  const [battleTag, setBattleTag] = useState("");
  const [profile, setProfile] = useState<PlayerProfile | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedTag = battleTag.trim();

    if (!battleTagPattern.test(trimmedTag)) {
      setProfile(null);
      setError("Enter a BattleTag in the format username-1234.");
      return;
    }

    setIsLoading(true);
    setError("");
    setProfile(null);

    try {
      setProfile(await getPlayer(trimmedTag));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to load player",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="lookup-panel" aria-label="Player search">
      <form className="search-form" onSubmit={handleSubmit}>
        <label htmlFor="battle-tag">BattleTag</label>
        <div className="search-row">
          <input
            id="battle-tag"
            name="battleTag"
            type="text"
            value={battleTag}
            onChange={(event) => setBattleTag(event.target.value)}
            placeholder="username-1234"
            required
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? "Searching..." : "Find player"}
          </button>
        </div>
      </form>

      <div id="search-status" aria-live="polite">
        {error && <p className="status-message error-message">{error}</p>}
      </div>

      {profile && <PLayerCard profile={profile} />}
    </section>
  );
}

export default Search;
