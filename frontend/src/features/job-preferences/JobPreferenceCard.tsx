import { Badge, Button, Group, Paper, Stack, Text } from "@mantine/core";

import type { JobPreferenceResponse, WorkMode } from "./types.ts";

type JobPreferenceCardProps = {
  preference: JobPreferenceResponse;
  isMarkedForDeletion?: boolean;
  onEdit: () => void;
  onRemove: () => void;
  disabled: boolean;
};

const workModeLabels: Record<WorkMode, string> = {
  remote: "Remote",
  hybrid: "Hybrid",
  office: "Office",
};

export function JobPreferenceCard({
  preference,
  onEdit,
  onRemove,
  disabled,
  isMarkedForDeletion = false,
}: JobPreferenceCardProps) {
  return (
    <Paper
      withBorder
      p="md"
      radius="md"
      bg={isMarkedForDeletion ? "red.0" : undefined}
    >
      <Stack gap="md">
        <Group justify="space-between" align="flex-start">
          <div>
            <Text fw={600} size="lg">
              {preference.target_title}
            </Text>
            <Text c="dimmed" size="sm">
              Preferred work modes
            </Text>
          </div>

          <Group gap="xs">
            <Button
              type="button"
              variant="default"
              size="xs"
              disabled={disabled || isMarkedForDeletion}
              onClick={onEdit}
            >
              Edit
            </Button>

            <Button
              type="button"
              color={isMarkedForDeletion ? "green" : "red"}
              variant="light"
              size="xs"
              disabled={disabled}
              onClick={onRemove}
            >
              {isMarkedForDeletion ? `Add back` : `Remove`}
            </Button>
          </Group>
        </Group>

        {isMarkedForDeletion && (
          <Text c="red" size="sm">
            This preference will be removed when you save changes.
          </Text>
        )}

        <Stack gap="xs">
          <Text fw={500} size="sm">
            Keywords
          </Text>

          <Group gap="xs">
            {preference.keywords.map((keyword) => (
              <Badge key={keyword} variant="light">
                {keyword}
              </Badge>
            ))}
          </Group>
        </Stack>

        <Stack gap="xs">
          <Text fw={500} size="sm">
            Work modes
          </Text>

          <Group gap="xs">
            {preference.accepted_work_modes.map((workMode) => (
              <Badge key={workMode} color="teal" variant="light">
                {workModeLabels[workMode]}
              </Badge>
            ))}
          </Group>
        </Stack>
      </Stack>
    </Paper>
  );
}
