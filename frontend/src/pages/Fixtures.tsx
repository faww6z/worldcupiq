import { useMemo, useState } from "react";

import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import MatchCard from "../components/MatchCard";
import { useMatches } from "../hooks/useMatches";

const GROUPS = ["", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"];

export default function Fixtures() {
  const [groupCode, setGroupCode] = useState("");
  const [teamCode, setTeamCode] = useState("");
  const { matches, isLoading, error } = useMatches({ groupCode, teamCode });

  const availableDates = useMemo(() => {
    return Array.from(new Set(matches.map((match) => match.date)));
  }, [matches]);

  return (
    <div className="mx-auto grid max-w-7xl gap-6 px-4 py-8 lg:px-8">
      <div className="flex flex-col gap-2">
        <p className="text-sm font-black uppercase text-clay">Fixtures</p>
        <h1 className="text-3xl font-black tracking-normal">Group Stage Schedule</h1>
      </div>

      <section className="grid gap-3 rounded border border-black/10 bg-white p-4 shadow-sm md:grid-cols-[220px_1fr_auto] md:items-end">
        <label className="grid gap-1 text-sm font-bold">
          Group
          <select
            value={groupCode}
            onChange={(event) => setGroupCode(event.target.value)}
            className="rounded border border-black/15 bg-white px-3 py-2"
          >
            {GROUPS.map((group) => (
              <option key={group || "all"} value={group}>
                {group ? `Group ${group}` : "All groups"}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-bold">
          Team code
          <input
            value={teamCode}
            onChange={(event) => setTeamCode(event.target.value.toUpperCase())}
            placeholder="MEX"
            className="rounded border border-black/15 bg-white px-3 py-2 uppercase"
            maxLength={3}
          />
        </label>
        <button
          type="button"
          onClick={() => {
            setGroupCode("");
            setTeamCode("");
          }}
          className="rounded border border-black/15 px-4 py-2 text-sm font-black hover:bg-black/5"
        >
          Clear
        </button>
      </section>

      {availableDates.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {availableDates.map((date) => (
            <span key={date} className="rounded bg-black/5 px-3 py-1 text-xs font-bold text-black/60">
              {date}
            </span>
          ))}
        </div>
      )}

      {isLoading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!isLoading && !error && matches.length === 0 && (
        <div className="rounded border border-black/10 bg-white p-6 text-sm font-semibold text-black/60">
          No fixtures match those filters.
        </div>
      )}
      {!isLoading && !error && matches.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {matches.map((match) => (
            <MatchCard key={match.id} match={match} />
          ))}
        </div>
      )}
    </div>
  );
}

