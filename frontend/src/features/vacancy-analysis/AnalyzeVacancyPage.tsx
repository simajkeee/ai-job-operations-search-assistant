import {
  Alert,
  Anchor,
  Button,
  Container,
  Paper,
  Stack,
  Text,
  Textarea,
  TextInput,
  Title,
} from "@mantine/core";

import { useForm } from "@mantine/form";
import { useState } from "react";
import { Link } from "react-router-dom";

import { ApiError } from "../../shared/api/ApiError.ts";
import { useAuth } from "../auth/useAuth.ts";
import { analyzeVacancy } from "./api.ts";
import { AnalysisResult } from "./AnalysisResult.tsx";
import type { VacancyAnalyzeRequest, VacancyAnalyzeResponse } from "./types.ts";

export function AnalyzeVacancyPage() {
  const { accessToken, logout } = useAuth();

  const [analysis, setAnalysis] = useState<VacancyAnalyzeResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [requiresPreferences, setRequiresPreferences] = useState(false);

  const form = useForm<VacancyAnalyzeRequest>({
    initialValues: {
      vacancy_title: "",
      vacancy_text: "",
    },
    validate: {
      vacancy_title: (value) =>
        value.trim().length > 0 ? null : "Enter the vacancy title",
      vacancy_text: (value) =>
        value.trim().length > 0 ? null : "Enter the vacancy description",
    },
  });

  async function handleSubmit(values: VacancyAnalyzeRequest): Promise<void> {
    if (accessToken === null) {
      return;
    }

    setAnalysis(null);
    setErrorMessage(null);
    setRequiresPreferences(false);

    try {
      const result = await analyzeVacancy(accessToken, {
        vacancy_title: values.vacancy_title.trim(),
        vacancy_text: values.vacancy_text.trim(),
      });

      setAnalysis(result);
    } catch (error: unknown) {
      if (error instanceof ApiError && error.status === 401) {
        logout();
        return;
      }

      if (error instanceof ApiError && error.status === 409) {
        setErrorMessage(
          "Create at least one job preference before analyzing vacancies.",
        );
        setRequiresPreferences(true);
        return;
      }

      if (error instanceof ApiError && error.status === 502) {
        setErrorMessage(
          "The analysis provider returned an invalid result. Please try again.",
        );
        return;
      }

      setErrorMessage(
        error instanceof Error ? error.message : "Could not analyze vacancy",
      );
    }
  }

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={1}>Analyze vacancy</Title>
          <Text c="dimmed">
            Paste a vacancy to evaluate it against your job preferences.
          </Text>
        </div>

        <Paper withBorder p="lg" radius="md">
          <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
            <Stack>
              <TextInput
                label="Vacancy title"
                placeholder="Senior PHP Developer"
                withAsterisk
                disabled={form.submitting}
                {...form.getInputProps("vacancy_title")}
              />

              <Textarea
                label="Vacancy description"
                placeholder="Paste the full vacancy description here…"
                rows={10}
                resize="none"
                withAsterisk
                disabled={form.submitting}
                {...form.getInputProps("vacancy_text")}
              />

              <Button type="submit" loading={form.submitting}>
                Analyze vacancy
              </Button>
            </Stack>
          </form>
        </Paper>

        {errorMessage !== null && (
          <Alert color="red" title="Could not analyze vacancy">
            <Stack gap="xs">
              <Text>{errorMessage}</Text>

              {requiresPreferences && (
                <Anchor component={Link} to="/preferences">
                  Create job preferences
                </Anchor>
              )}
            </Stack>
          </Alert>
        )}

        {analysis !== null && <AnalysisResult analysis={analysis} />}
      </Stack>
    </Container>
  );
}
