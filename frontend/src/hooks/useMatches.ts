import { useEffect, useState } from "react";

import { getMatches, getUpcomingMatches } from "../api/matches";
import type { Match } from "../types/match";

type UseMatchesOptions = {
  upcomingOnly?: boolean;
  groupCode?: string;
  teamCode?: string;
};

export function useMatches({ upcomingOnly = false, groupCode, teamCode }: UseMatchesOptions = {}) {
  const [matches, setMatches] = useState<Match[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);
    setError(null);

    const request = upcomingOnly
      ? getUpcomingMatches()
      : getMatches({
          group_code: groupCode || undefined,
          team_code: teamCode || undefined,
        });

    request
      .then((data) => {
        if (isMounted) {
          setMatches(data);
        }
      })
      .catch((requestError: unknown) => {
        if (isMounted) {
          const message = requestError instanceof Error ? requestError.message : "Unknown request error";
          setError(message);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [groupCode, teamCode, upcomingOnly]);

  return { matches, isLoading, error };
}

