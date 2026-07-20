import {
  Alert,
  Center,
  Container,
  Loader,
  Stack,
  Text,
  Title,
  Button,
  Group,
} from "@mantine/core";

import { useAuth } from "../auth/useAuth.ts";
import { useEffect, useState } from "react";
import { getJobPreferences, replaceJobPreferences } from "./api.ts";
import type {
  JobPreferenceInput,
  JobPreferenceResponse,
  ReplaceJobPreferencesRequest,
} from "./types.ts";
import { ApiError } from "../../shared/api/ApiError.ts";
import { useForm } from "@mantine/form";
import { JobPreferenceEditor } from "./JobPreferenceEditor.tsx";
import { JobPreferenceCard } from "./JobPreferenceCard.tsx";

function isSavedJobPreference(
  preference: JobPreferenceInput,
): preference is JobPreferenceResponse {
  return preference.id !== null;
}

function createEmptyJobPreference(): JobPreferenceInput {
  return {
    id: null,
    target_title: "",
    keywords: [],
    accepted_work_modes: [],
    resume_label: null,
  };
}

export function JobPreferencesPage() {
  const { accessToken, logout } = useAuth();
  const [isInitializing, setIsInitializing] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [saveErrorMessage, setSaveErrorMessage] = useState<string | null>(null);
  const [saveSuccessMessage, setSaveSuccessMessage] = useState<string | null>(
    null,
  );
  const [editingPreferenceId, setEditingPreferenceId] = useState<string | null>(
    null,
  );
  const [deletedPreferenceIds, setDeletedPreferenceIds] = useState<Set<string>>(
    () => new Set(),
  );
  const form = useForm<ReplaceJobPreferencesRequest>({
    initialValues: {
      preferences: [],
    },
    validate: {
      preferences: {
        target_title: (value) =>
          value.trim().length > 0 ? null : "Target role is required",
        keywords: (value) =>
          value.length > 0 ? null : "At least one keyword is required",
        accepted_work_modes: (value) =>
          value.length > 0 ? null : "Select at least one work mode",
      },
    },
  });
  const { resetDirty, setValues } = form;

  async function savePreferences(
    values: ReplaceJobPreferencesRequest,
  ): Promise<void> {
    if (accessToken === null) {
      return;
    }

    setSaveSuccessMessage(null);
    setSaveErrorMessage(null);

    try {
      const preferencesToSave = values.preferences.filter(
        (preference) =>
          preference.id === null || !deletedPreferenceIds.has(preference.id),
      );
      const savedPreferences = await replaceJobPreferences(accessToken, {
        preferences: preferencesToSave,
      });
      setSaveSuccessMessage("Preferences saved");
      setValues({
        preferences: savedPreferences,
      });
      resetDirty({
        preferences: savedPreferences,
      });
      setDeletedPreferenceIds(new Set());
      setEditingPreferenceId(null);
    } catch (error: unknown) {
      if (error instanceof ApiError && error.status === 401) {
        logout();
        return;
      }

      setSaveErrorMessage(
        error instanceof Error ? error.message : "Could not save preferences",
      );
    }
  }

  useEffect(() => {
    if (saveSuccessMessage === null) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      setSaveSuccessMessage(null);
    }, 3000);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [saveSuccessMessage]);

  useEffect(() => {
    if (accessToken === null) {
      return;
    }

    let isActive = true;

    getJobPreferences(accessToken)
      .then((preferences: JobPreferenceResponse[]) => {
        if (!isActive) {
          return;
        }

        setValues({
          preferences,
        });
        resetDirty({ preferences });

        setIsInitializing(false);
      })
      .catch((error: unknown) => {
        if (!isActive) {
          return;
        }

        if (error instanceof ApiError && error.status === 401) {
          logout();
          return;
        }

        setErrorMessage(
          error instanceof Error ? error.message : "Could not load preferences",
        );
      })
      .finally(() => {
        if (!isActive) {
          return;
        }
        setIsInitializing(false);
      });

    return () => {
      isActive = false;
    };
  }, [accessToken, logout, resetDirty, setValues]);

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Group justify="space-between" align="flex-start" wrap="wrap">
          <div>
            <Title order={1}>Job preferences</Title>
            <Text c="dimmed">
              Define the roles, skills, and work modes that fit your search.
            </Text>
          </div>

          <Button
            type="button"
            disabled={isInitializing || form.submitting}
            onClick={() => {
              form.insertListItem("preferences", createEmptyJobPreference());
            }}
          >
            Add preference
          </Button>
        </Group>

        {saveSuccessMessage !== null && (
          <Alert color="green" title="Saved">
            {saveSuccessMessage}
          </Alert>
        )}

        {isInitializing ? (
          <Center py="xl">
            <Stack align="center" gap="sm">
              <Loader />
              <Text c="dimmed">Loading preferences…</Text>
            </Stack>
          </Center>
        ) : errorMessage !== null ? (
          <Alert color="red" title="Could not load preferences">
            {errorMessage}
          </Alert>
        ) : form.values.preferences.length === 0 ? (
          <Alert color="blue" title="No preferences yet">
            Add a job preference to start analyzing vacancies.
          </Alert>
        ) : (
          <form onSubmit={form.onSubmit(savePreferences)}>
            <Stack gap="md">
              {form.values.preferences.map((preference, index) => {
                const isSavedPreference = isSavedJobPreference(preference);
                const isEditing = preference.id === editingPreferenceId;

                if (isSavedPreference && !isEditing) {
                  return (
                    <JobPreferenceCard
                      key={preference.id}
                      preference={preference}
                      disabled={form.submitting}
                      isMarkedForDeletion={deletedPreferenceIds.has(
                        preference.id,
                      )}
                      onEdit={() => {
                        setEditingPreferenceId(preference.id);
                      }}
                      onRemove={() => {
                        setDeletedPreferenceIds((current) => {
                          const newSet = new Set(current);
                          if (newSet.has(preference.id)) {
                            newSet.delete(preference.id);
                          } else {
                            newSet.add(preference.id);
                          }
                          return newSet;
                        });
                      }}
                    />
                  );
                }

                return (
                  <JobPreferenceEditor
                    key={preference.id ?? `new-${index}`}
                    preference={preference}
                    disabled={form.submitting}
                    validationErrors={{
                      targetTitle:
                        form.errors[`preferences.${index}.target_title`],
                      keywords: form.errors[`preferences.${index}.keywords`],
                      acceptedWorkModes:
                        form.errors[`preferences.${index}.accepted_work_modes`],
                    }}
                    onChange={(updatedPreference) => {
                      form.setFieldValue(
                        `preferences.${index}`,
                        updatedPreference,
                      );
                    }}
                    onRemove={() => {
                      if (isSavedPreference) {
                        setDeletedPreferenceIds((current) => {
                          const next = new Set(current);
                          next.add(preference.id);
                          return next;
                        });
                        setEditingPreferenceId(null);
                        return;
                      }

                      form.removeListItem("preferences", index);
                    }}
                    onClose={
                      isSavedPreference
                        ? () => {
                            setEditingPreferenceId(null);
                          }
                        : undefined
                    }
                  />
                );
              })}

              {saveErrorMessage !== null && (
                <Alert color="red" title="Could not save preferences">
                  {saveErrorMessage}
                </Alert>
              )}

              <Button
                type="submit"
                loading={form.submitting}
                disabled={!form.isDirty() && deletedPreferenceIds.size === 0}
              >
                Save changes
              </Button>
            </Stack>
          </form>
        )}
      </Stack>
    </Container>
  );
}
