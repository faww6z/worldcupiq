import type { Prediction } from "../types/prediction";
import { formatPercent } from "../utils/format";

type ProbabilityBarsProps = {
  prediction: Prediction;
};

export default function ProbabilityBars({ prediction }: ProbabilityBarsProps) {
  const rows = [
    { label: prediction.team_a.name, value: prediction.team_a_win_prob, color: "bg-pitch" },
    { label: "Draw", value: prediction.draw_prob, color: "bg-gold" },
    { label: prediction.team_b.name, value: prediction.team_b_win_prob, color: "bg-clay" },
  ];

  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-black tracking-normal">Win Probability</h2>
      <div className="mt-4 grid gap-4">
        {rows.map((row) => (
          <div key={row.label} className="grid gap-1.5">
            <div className="flex items-center justify-between gap-3 text-sm font-bold">
              <span>{row.label}</span>
              <span>{formatPercent(row.value)}</span>
            </div>
            <div className="h-3 overflow-hidden rounded bg-black/10">
              <div className={`h-full rounded ${row.color}`} style={{ width: formatPercent(row.value) }} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

