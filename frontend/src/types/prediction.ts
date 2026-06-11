import type { TeamSummary } from "./match";

export type PredictedScore = {
  team_a: number;
  team_b: number;
};

export type ScorelineProbability = {
  score: string;
  probability: number;
};

export type Prediction = {
  match_id: number;
  model_version: string;
  team_a: TeamSummary;
  team_b: TeamSummary;
  team_a_win_prob: number;
  draw_prob: number;
  team_b_win_prob: number;
  expected_goals_a: number;
  expected_goals_b: number;
  predicted_score: PredictedScore;
  top_scorelines: ScorelineProbability[];
  confidence_label: "low" | "medium" | "high";
  explanation: string[];
};

