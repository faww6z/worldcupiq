import type { Prediction } from "../types/prediction";
import { formatPercent } from "../utils/format";

type ScorelineTableProps = {
  prediction: Prediction;
};

export default function ScorelineTable({ prediction }: ScorelineTableProps) {
  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-black tracking-normal">Top Scorelines</h2>
      <div className="mt-4 overflow-hidden rounded border border-black/10">
        <table className="w-full text-left text-sm">
          <thead className="bg-black/5 text-xs uppercase text-black/50">
            <tr>
              <th className="px-3 py-2">Score</th>
              <th className="px-3 py-2 text-right">Probability</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-black/10">
            {prediction.top_scorelines.map((scoreline) => (
              <tr key={scoreline.score}>
                <td className="px-3 py-2 font-black">{scoreline.score}</td>
                <td className="px-3 py-2 text-right font-semibold">{formatPercent(scoreline.probability)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

