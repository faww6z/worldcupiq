export type TeamSummary = {
  id: number;
  code: string;
  name: string;
};

export type Match = {
  id: number;
  match_code: string;
  date: string;
  time_utc: string | null;
  stage: string;
  group_code: string | null;
  team_a: TeamSummary;
  team_b: TeamSummary;
  venue: string | null;
  city: string | null;
  status: "scheduled" | "live" | "finished" | "postponed";
  score_a: number | null;
  score_b: number | null;
};

