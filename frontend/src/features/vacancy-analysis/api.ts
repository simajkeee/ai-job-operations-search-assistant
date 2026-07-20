import type { VacancyAnalyzeRequest, VacancyAnalyzeResponse } from "./types.ts";
import { request } from "../../shared/api/httpClient.ts";

const ANALYZE_API_PATH = "/api/v1/vacancies/analyze";

export function analyzeVacancy(
  accessToken: string,
  vacancyAnalyzeRequest: VacancyAnalyzeRequest,
): Promise<VacancyAnalyzeResponse> {
  return request<VacancyAnalyzeResponse>(ANALYZE_API_PATH, {
    accessToken,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(vacancyAnalyzeRequest),
  });
}
