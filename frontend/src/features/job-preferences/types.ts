export type WorkMode = "remote" | "hybrid" | "office";

export type JobPreferenceResponse = {
  id: string;
  target_title: string;
  keywords: string[];
  accepted_work_modes: WorkMode[];
  resume_label: string | null;
};

export type JobPreferenceInput = Omit<JobPreferenceResponse, "id"> & {
  id: string | null;
};

export type ReplaceJobPreferencesRequest = {
  preferences: JobPreferenceInput[];
};
