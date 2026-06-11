import { apiClient } from "./client";
import type { Match } from "../types/match";

export async function getUpcomingMatches(): Promise<Match[]> {
  const response = await apiClient.get<Match[]>("/matches/upcoming");
  return response.data;
}

export async function getMatches(params?: {
  group_code?: string;
  team_code?: string;
  status?: string;
}): Promise<Match[]> {
  const response = await apiClient.get<Match[]>("/matches", { params });
  return response.data;
}

export async function getMatch(matchId: string): Promise<Match> {
  const response = await apiClient.get<Match>(`/matches/${matchId}`);
  return response.data;
}

