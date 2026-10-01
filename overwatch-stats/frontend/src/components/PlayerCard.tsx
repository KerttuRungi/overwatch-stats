import { useState } from "react";
import { Plus, X } from "lucide-react";
import type { PlayerProfile } from "../../types";
import { addPlayerToList } from "../api/routes/addPlayerToList";
import { removePlayerFromList } from "../api/routes/removePlayerFromList";

type PlayerCardProps = {
  profile: PlayerProfile;
  isInList: boolean;
  onListChanged?: () => void;
};

export default function PLayerCard({
  profile,
  isInList,
  onListChanged,
}: PlayerCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAddPlayer() {
    setIsLoading(true);
    setError("");

    if (!profile) {
      setIsLoading(false);
      setError("No player to add player to list.");
      return;
    }

    try {
      await addPlayerToList(profile.summary);
      onListChanged?.();
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Unable to add player to list",
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleRemovePlayer() {
    setIsLoading(true);
    setError("");

    try {
      await removePlayerFromList(profile.summary.username);
      onListChanged?.();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to remove player from list",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="profile-card">
      <img className="profile-banner" src={profile.summary.namecard} alt="" />
      <div className="profile-content">
        <img
          className="profile-avatar"
          src={profile.summary.avatar}
          alt={`${profile.summary.username} avatar`}
        />
        <div>
          <p className="profile-label">Player profile</p>
          <h2>{profile.summary.username}</h2>
        </div>
        <div className="endorsement">
          <span>Endorsement</span>
          {/* <strong>{profile.summary.endorsement.level}</strong> */}
        </div>
        <div className="">
          <button
            onClick={handleAddPlayer}
            disabled={isLoading}
            type="button"
            aria-label="Add player to list"
          >
            {isLoading ? "Adding..." : <Plus />}
          </button>
        </div>
        {error && <p>{error}</p>}
      </div>
    </div>
  );
}
