import { useCallback, useEffect, useState } from "react";
import type { PlayerProfileSummary } from "../../types";
import { getAllPlayer } from "../api/routes/getPlayer";

function toMessage(requestError: unknown) {
  return requestError instanceof Error
    ? requestError.message
    : "Unable to load players";
}

export function usePlayerList() {
  const [players, setPlayers] = useState<PlayerProfileSummary[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const reload = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      setPlayers(await getAllPlayer());
    } catch (requestError) {
      setError(toMessage(requestError));
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial load: state is only set after the request resolves.
  useEffect(() => {
    let cancelled = false;

    getAllPlayer()
      .then((result) => {
        if (!cancelled) setPlayers(result);
      })
      .catch((requestError) => {
        if (!cancelled) setError(toMessage(requestError));
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { players, error, isLoading, reload };
}
