import type { Prediction } from "../types/prediction";

type PredictionCardProps = {
  prediction: Prediction;
};

export default function PredictionCard({ prediction }: PredictionCardProps) {
  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-black uppercase text-clay">Predicted Score</p>
          <div className="mt-3 grid grid-cols-[1fr_auto_1fr] items-center gap-4">
            <div>
              <p className="text-xs font-bold text-black/45">{prediction.team_a.code}</p>
              <p className="text-xl font-black">{prediction.team_a.name}</p>
            </div>
            <div className="rounded bg-pitch px-4 py-2 text-3xl font-black text-white">
              {prediction.predicted_score.team_a}-{prediction.predicted_score.team_b}
            </div>
            <div className="text-right">
              <p className="text-xs font-bold text-black/45">{prediction.team_b.code}</p>
              <p className="text-xl font-black">{prediction.team_b.name}</p>
            </div>
          </div>
        </div>
        <span className="rounded bg-mint px-3 py-1 text-xs font-black uppercase text-pitch">
          {prediction.confidence_label} confidence
        </span>
      </div>
      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="rounded bg-black/5 p-3">
          <p className="text-xs font-bold uppercase text-black/45">{prediction.team_a.code} xG</p>
          <p className="mt-1 text-2xl font-black">{prediction.expected_goals_a.toFixed(2)}</p>
        </div>
        <div className="rounded bg-black/5 p-3 text-right">
          <p className="text-xs font-bold uppercase text-black/45">{prediction.team_b.code} xG</p>
          <p className="mt-1 text-2xl font-black">{prediction.expected_goals_b.toFixed(2)}</p>
        </div>
      </div>
    </section>
  );
}

