import { useCallback, useEffect, useState } from "react";
import type { PlayerProfileSummary } from "../../types";
import { getAllPlayer } from "../api/routes/getPlayer";

export function usePlayerList() {
  const [players, setPlayers] = useState<PlayerProfileSummary[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const reload = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      setPlayers(await getAllPlayer());
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to load players",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  return { players, error, isLoading, reload };
}
