import { Navigate, Route, Routes } from "react-router-dom";

import { LoginPage } from "../features/auth/LoginPage.tsx";
import { RegisterPage } from "../features/auth/RegisterPage.tsx";
import { JobPreferencesPage } from "../features/job-preferences/JobPreferencesPage.tsx";
import { AnalyzeVacancyPage } from "../features/vacancy-analysis/AnalyzeVacancyPage.tsx";
import { ProtectedRoute } from "../features/auth/ProtectedRoute.tsx";
import { AppLayout } from "./AppLayout.tsx";

export function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/preferences" replace />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/preferences" element={<JobPreferencesPage />} />
          <Route path="/analyze" element={<AnalyzeVacancyPage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/preferences" replace />} />
    </Routes>
  );
}
