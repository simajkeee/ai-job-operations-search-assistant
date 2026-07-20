import type { WorkMode } from "../job-preferences/types.ts";

export type VacancyAnalyzeRequest = {
  vacancy_title: string;
  vacancy_text: string;
};

export type Decision = "apply" | "apply_with_caveats" | "skip";

export type RoleMatch = "strong" | "partial" | "none";

export type VacancyAnalyzeResponse = {
  decision: Decision;
  recommended_resume: string | null;
  matched_job_preference_id: string | null;
  interpreted_role: string | null;
  role_match: RoleMatch;
  role_evidence: string[];
  matched_keywords: string[];
  unmatched_preference_keywords: string[];
  detected_work_modes: WorkMode[];
  work_mode_match: boolean | null;
  critical_gaps: string[];
  reasoning: string;
};
