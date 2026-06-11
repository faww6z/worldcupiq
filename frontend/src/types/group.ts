export type GroupSummary = {
  id: number;
  code: string;
  name: string;
};

export type GroupTableRow = {
  rank: number;
  team_id: number;
  team_code: string;
  team_name: string;
  played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
};

export type GroupTable = {
  group_code: string;
  rows: GroupTableRow[];
};

