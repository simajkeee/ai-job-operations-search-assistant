import type {
  JobPreferenceResponse,
  ReplaceJobPreferencesRequest,
} from "./types.ts";
import { request } from "../../shared/api/httpClient.ts";

const JOB_PREFERENCES_API_PATH = "/api/v1/job-preferences";

export function getJobPreferences(
  accessToken: string,
): Promise<JobPreferenceResponse[]> {
  return request<JobPreferenceResponse[]>(`${JOB_PREFERENCES_API_PATH}`, {
    accessToken,
  });
}

export function replaceJobPreferences(
  accessToken: string,
  data: ReplaceJobPreferencesRequest,
): Promise<JobPreferenceResponse[]> {
  return request<JobPreferenceResponse[]>(`${JOB_PREFERENCES_API_PATH}`, {
    accessToken,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}
