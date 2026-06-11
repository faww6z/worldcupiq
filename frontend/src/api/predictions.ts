import { apiClient } from "./client";
import type { Prediction } from "../types/prediction";

export async function getPrediction(matchId: string): Promise<Prediction> {
  const response = await apiClient.get<Prediction>(`/predictions/${matchId}`);
  return response.data;
}

