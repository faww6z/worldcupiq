import { apiClient } from "./client";
import type { GroupSummary, GroupTable } from "../types/group";

export async function getGroups(): Promise<GroupSummary[]> {
  const response = await apiClient.get<GroupSummary[]>("/groups");
  return response.data;
}

export async function getGroupTable(groupCode: string): Promise<GroupTable> {
  const response = await apiClient.get<GroupTable>(`/groups/${groupCode}/table`);
  return response.data;
}

