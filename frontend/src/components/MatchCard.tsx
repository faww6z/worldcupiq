import { Link } from "react-router-dom";

import type { Match } from "../types/match";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    weekday: "short",
    month: "short",
    day: "numeric",
  }).format(new Date(`${value}T12:00:00Z`));
}

function formatTime(value: string | null) {
  if (!value) return "Time TBD";
  return new Intl.DateTimeFormat("en", {
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  }).format(new Date(value));
}

type MatchCardProps = {
  match: Match;
};

export default function MatchCard({ match }: MatchCardProps) {
  return (
    <Link
      to={`/matches/${match.id}`}
      className="group grid min-h-32 gap-4 rounded border border-black/10 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:border-pitch/30 hover:shadow-panel"
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="rounded bg-mint px-2.5 py-1 text-xs font-black uppercase text-pitch">
          Group {match.group_code ?? "TBD"}
        </span>
        <span className="text-xs font-semibold uppercase text-black/50">{match.status}</span>
      </div>
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        <div>
          <p className="text-xs font-bold text-black/45">{match.team_a.code}</p>
          <p className="text-lg font-black">{match.team_a.name}</p>
        </div>
        <span className="rounded bg-black/5 px-2 py-1 text-xs font-black text-black/50">vs</span>
        <div className="text-right">
          <p className="text-xs font-bold text-black/45">{match.team_b.code}</p>
          <p className="text-lg font-black">{match.team_b.name}</p>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-2 text-sm text-black/60">
        <span>{formatDate(match.date)} · {formatTime(match.time_utc)}</span>
        <span>{match.venue ?? "Venue TBD"}{match.city ? `, ${match.city}` : ""}</span>
      </div>
    </Link>
  );
}

