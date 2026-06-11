import type { Match } from "../types/match";
import type { GroupTable, GroupTableRow } from "../types/group";
import type { Prediction } from "../types/prediction";

type ProjectedRow = GroupTableRow & {
  projectedRank: number;
  rankChange: number;
};

type GroupImpactProps = {
  match: Match;
  prediction: Prediction;
  table: GroupTable;
};

function cloneRow(row: GroupTableRow): GroupTableRow {
  return { ...row };
}

function applyProjectedResult(row: GroupTableRow, goalsFor: number, goalsAgainst: number) {
  row.played += 1;
  row.goals_for += goalsFor;
  row.goals_against += goalsAgainst;
  row.goal_difference = row.goals_for - row.goals_against;
  if (goalsFor > goalsAgainst) {
    row.wins += 1;
    row.points += 3;
  } else if (goalsFor === goalsAgainst) {
    row.draws += 1;
    row.points += 1;
  } else {
    row.losses += 1;
  }
}

function projectRows(match: Match, prediction: Prediction, table: GroupTable): ProjectedRow[] {
  const rows = table.rows.map(cloneRow);
  const teamA = rows.find((row) => row.team_id === match.team_a.id);
  const teamB = rows.find((row) => row.team_id === match.team_b.id);

  if (teamA && teamB) {
    applyProjectedResult(teamA, prediction.predicted_score.team_a, prediction.predicted_score.team_b);
    applyProjectedResult(teamB, prediction.predicted_score.team_b, prediction.predicted_score.team_a);
  }

  const sorted = [...rows].sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points;
    if (b.goal_difference !== a.goal_difference) return b.goal_difference - a.goal_difference;
    if (b.goals_for !== a.goals_for) return b.goals_for - a.goals_for;
    return a.team_name.localeCompare(b.team_name);
  });

  return sorted.map((row, index) => ({
    ...row,
    projectedRank: index + 1,
    rankChange: row.rank - (index + 1),
  }));
}

function rankText(rankChange: number) {
  if (rankChange > 0) return `up ${rankChange}`;
  if (rankChange < 0) return `down ${Math.abs(rankChange)}`;
  return "no change";
}

export default function GroupImpact({ match, prediction, table }: GroupImpactProps) {
  const projectedRows = projectRows(match, prediction, table);
  const impactedRows = projectedRows.filter(
    (row) => row.team_id === match.team_a.id || row.team_id === match.team_b.id,
  );

  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-black tracking-normal">Group Impact</h2>
        <span className="rounded bg-gold px-3 py-1 text-xs font-black uppercase text-black/70">
          predicted result
        </span>
      </div>
      <p className="mt-3 text-sm font-semibold text-black/60">
        If the {prediction.predicted_score.team_a}-{prediction.predicted_score.team_b} prediction happens:
      </p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {impactedRows.map((row) => (
          <div key={row.team_id} className="rounded bg-black/5 p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-black">{row.team_name}</p>
                <p className="mt-1 text-xs font-bold uppercase text-black/45">
                  Rank {row.rank} to {row.projectedRank} · {rankText(row.rankChange)}
                </p>
              </div>
              <p className="text-2xl font-black">{row.points}</p>
            </div>
            <p className="mt-2 text-xs font-semibold text-black/50">
              {row.played} played · GD {row.goal_difference >= 0 ? "+" : ""}
              {row.goal_difference}
            </p>
          </div>
        ))}
      </div>
      <p className="mt-4 text-xs font-semibold text-black/45">
        This is a single predicted-result scenario, not a tournament simulation.
      </p>
    </section>
  );
}

