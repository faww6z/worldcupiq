import type { Prediction } from "../types/prediction";

type ExplanationPanelProps = {
  prediction: Prediction;
};

export default function ExplanationPanel({ prediction }: ExplanationPanelProps) {
  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-black tracking-normal">Why This Prediction?</h2>
      <ul className="mt-4 grid gap-3">
        {prediction.explanation.map((item) => (
          <li key={item} className="rounded bg-black/5 px-3 py-2 text-sm font-semibold text-black/70">
            {item}
          </li>
        ))}
      </ul>
      <p className="mt-4 text-xs font-semibold text-black/45">
        MVP model: seeded Elo-style ratings plus a Poisson scoreline matrix. It is not using live form,
        injuries, lineups, or historical backtesting yet.
      </p>
    </section>
  );
}

