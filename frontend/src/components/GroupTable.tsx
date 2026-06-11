import type { GroupTable as GroupTableType } from "../types/group";

type GroupTableProps = {
  table: GroupTableType;
};

export default function GroupTable({ table }: GroupTableProps) {
  return (
    <section className="rounded border border-black/10 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-black tracking-normal">Group {table.group_code} Table</h2>
        <span className="text-xs font-black uppercase text-black/45">Current</span>
      </div>
      <div className="mt-4 overflow-x-auto rounded border border-black/10">
        <table className="w-full min-w-[620px] text-left text-sm">
          <thead className="bg-black/5 text-xs uppercase text-black/50">
            <tr>
              <th className="px-3 py-2">#</th>
              <th className="px-3 py-2">Team</th>
              <th className="px-3 py-2 text-right">P</th>
              <th className="px-3 py-2 text-right">W</th>
              <th className="px-3 py-2 text-right">D</th>
              <th className="px-3 py-2 text-right">L</th>
              <th className="px-3 py-2 text-right">GF</th>
              <th className="px-3 py-2 text-right">GA</th>
              <th className="px-3 py-2 text-right">GD</th>
              <th className="px-3 py-2 text-right">Pts</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-black/10">
            {table.rows.map((row) => (
              <tr key={row.team_id}>
                <td className="px-3 py-2 font-black text-black/50">{row.rank}</td>
                <td className="px-3 py-2">
                  <span className="font-black">{row.team_name}</span>
                  <span className="ml-2 text-xs font-bold text-black/40">{row.team_code}</span>
                </td>
                <td className="px-3 py-2 text-right font-semibold">{row.played}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.wins}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.draws}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.losses}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.goals_for}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.goals_against}</td>
                <td className="px-3 py-2 text-right font-semibold">{row.goal_difference}</td>
                <td className="px-3 py-2 text-right font-black">{row.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs font-semibold text-black/45">
        MVP sorting: points, goal difference, goals for, then team name.
      </p>
    </section>
  );
}

