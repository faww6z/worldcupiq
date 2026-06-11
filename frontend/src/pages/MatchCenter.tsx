import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getGroupTable } from "../api/groups";
import { getMatch } from "../api/matches";
import { getPrediction } from "../api/predictions";
import ErrorState from "../components/ErrorState";
import ExplanationPanel from "../components/ExplanationPanel";
import GroupImpact from "../components/GroupImpact";
import GroupTable from "../components/GroupTable";
import LoadingState from "../components/LoadingState";
import PredictionCard from "../components/PredictionCard";
import ProbabilityBars from "../components/ProbabilityBars";
import ScorelineTable from "../components/ScorelineTable";
import type { GroupTable as GroupTableType } from "../types/group";
import type { Match } from "../types/match";
import type { Prediction } from "../types/prediction";
import { formatDate, formatTime } from "../utils/format";

type MatchCenterState = {
  match: Match | null;
  prediction: Prediction | null;
  groupTable: GroupTableType | null;
  isLoading: boolean;
  error: string | null;
};

export default function MatchCenter() {
  const { matchId } = useParams();
  const [state, setState] = useState<MatchCenterState>({
    match: null,
    prediction: null,
    groupTable: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    let isMounted = true;
    if (!matchId) {
      setState({ match: null, prediction: null, groupTable: null, isLoading: false, error: "Missing match id" });
      return;
    }

    setState((current) => ({ ...current, isLoading: true, error: null }));
    Promise.all([getMatch(matchId), getPrediction(matchId)])
      .then(async ([match, prediction]) => {
        const groupTable = match.group_code ? await getGroupTable(match.group_code) : null;
        if (isMounted) {
          setState({ match, prediction, groupTable, isLoading: false, error: null });
        }
      })
      .catch((requestError: unknown) => {
        if (isMounted) {
          const message = requestError instanceof Error ? requestError.message : "Unknown request error";
          setState({ match: null, prediction: null, groupTable: null, isLoading: false, error: message });
        }
      });

    return () => {
      isMounted = false;
    };
  }, [matchId]);

  if (state.isLoading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-8 lg:px-8">
        <LoadingState label="Loading match prediction" />
      </div>
    );
  }

  if (state.error || !state.match || !state.prediction) {
    return (
      <div className="mx-auto grid max-w-4xl gap-4 px-4 py-8 lg:px-8">
        <Link to="/fixtures" className="text-sm font-black text-pitch hover:underline">
          Back to fixtures
        </Link>
        <ErrorState message={state.error ?? "Match prediction was not available."} />
      </div>
    );
  }

  const { match, prediction } = state;

  return (
    <div className="mx-auto grid max-w-7xl gap-6 px-4 py-8 lg:px-8">
      <Link to="/fixtures" className="text-sm font-black text-pitch hover:underline">
        Back to fixtures
      </Link>

      <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm font-black uppercase text-clay">Group {match.group_code ?? "TBD"}</p>
            <h1 className="mt-2 text-3xl font-black tracking-normal">
              {match.team_a.name} vs {match.team_b.name}
            </h1>
            <p className="mt-2 text-sm font-semibold text-black/55">
              {formatDate(match.date)} · {formatTime(match.time_utc)}
            </p>
          </div>
          <div className="rounded bg-black/5 px-3 py-2 text-right text-sm font-bold text-black/60">
            <p>{match.venue ?? "Venue TBD"}</p>
            <p>{match.city ?? "City TBD"}</p>
          </div>
        </div>
      </section>

      <div className="grid gap-5 lg:grid-cols-[1.15fr_0.85fr]">
        <div className="grid gap-5">
          <PredictionCard prediction={prediction} />
          <ProbabilityBars prediction={prediction} />
        </div>
        <div className="grid gap-5">
          <ScorelineTable prediction={prediction} />
          <ExplanationPanel prediction={prediction} />
        </div>
      </div>

      {state.groupTable && (
        <div className="grid gap-5 lg:grid-cols-[1fr_0.85fr]">
          <GroupTable table={state.groupTable} />
          <GroupImpact match={match} prediction={prediction} table={state.groupTable} />
        </div>
      )}

      <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-black tracking-normal">Model Version</h2>
        <p className="mt-2 text-sm font-semibold text-black/60">{prediction.model_version}</p>
      </section>
    </div>
  );
}
