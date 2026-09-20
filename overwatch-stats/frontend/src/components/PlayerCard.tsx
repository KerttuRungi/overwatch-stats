import { useState } from "react";
import { Plus } from "lucide-react";
import type { PlayerProfile } from "../../types";
import { addPlayerToList } from "../api/routes/addPlayerToList";

type PlayerCardProps = {
  profile: PlayerProfile;
};

export default function PLayerCard({ profile }: PlayerCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAddPlayer() {
    setIsLoading(true);
    setError("");

    if (!profile) {
      setIsLoading(true);
      setError("No player to add player to list.");
      return;
    }
    setIsLoading(true);
    setError("");

    try {
      await addPlayerToList(profile.summary);
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Unable to add player to list",
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
          <button onClick={handleAddPlayer} disabled={isLoading} type="button">
            {isLoading ? "Adding..." : <Plus />}
          </button>
        </div>
        {error && <p>{error}</p>}
      </div>
    </div>
  );
}
