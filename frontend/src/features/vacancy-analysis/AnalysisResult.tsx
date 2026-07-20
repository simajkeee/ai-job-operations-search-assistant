import {
  Alert,
  Badge,
  Divider,
  Group,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import type { Decision, RoleMatch, VacancyAnalyzeResponse } from "./types.ts";

type AnalysisResultProps = {
  analysis: VacancyAnalyzeResponse;
};

const decisionLabels: Record<Decision, string> = {
  apply: "Apply",
  apply_with_caveats: "Apply with caveats",
  skip: "Skip",
};

const decisionColors: Record<Decision, string> = {
  apply: "green",
  apply_with_caveats: "yellow",
  skip: "red",
};

const roleMatchLabels: Record<RoleMatch, string> = {
  strong: "Strong match",
  partial: "Partial match",
  none: "No role match",
};

function ValueBadges({ values }: { values: string[] }) {
  if (values.length === 0) {
    return <Text c="dimmed">None</Text>;
  }

  return (
    <Group gap="xs">
      {values.map((value) => (
        <Badge key={value} variant="light">
          {value}
        </Badge>
      ))}
    </Group>
  );
}

export function AnalysisResult({ analysis }: AnalysisResultProps) {
  return (
    <Paper withBorder p="lg" radius="md">
      <Stack gap="lg">
        <Group justify="space-between" align="flex-start">
          <div>
            <Text c="dimmed" size="sm">
              Analysis result
            </Text>
            <Title order={2}>
              {analysis.interpreted_role ?? "Role not identified"}
            </Title>
          </div>

          <Badge
            color={decisionColors[analysis.decision]}
            size="lg"
            variant="light"
          >
            {decisionLabels[analysis.decision]}
          </Badge>
        </Group>

        <Group gap="xl">
          <div>
            <Text c="dimmed" size="sm">
              Role match
            </Text>
            <Text fw={500}>{roleMatchLabels[analysis.role_match]}</Text>
          </div>

          <div>
            <Text c="dimmed" size="sm">
              Work mode match
            </Text>
            <Text fw={500}>
              {analysis.work_mode_match === null
                ? "Not specified"
                : analysis.work_mode_match
                  ? "Matches"
                  : "Does not match"}
            </Text>
          </div>

          <div>
            <Text c="dimmed" size="sm">
              Recommended resume
            </Text>
            <Text fw={500}>{analysis.recommended_resume ?? "None"}</Text>
          </div>
        </Group>

        <Divider />

        <Stack gap="xs">
          <Text fw={500}>Matched keywords</Text>
          <ValueBadges values={analysis.matched_keywords} />
        </Stack>

        <Stack gap="xs">
          <Text fw={500}>Missing preference keywords</Text>
          <ValueBadges values={analysis.unmatched_preference_keywords} />
        </Stack>

        <Stack gap="xs">
          <Text fw={500}>Detected work modes</Text>
          <ValueBadges values={analysis.detected_work_modes} />
        </Stack>

        <Stack gap="xs">
          <Text fw={500}>Role evidence</Text>
          <ValueBadges values={analysis.role_evidence} />
        </Stack>

        {analysis.critical_gaps.length > 0 && (
          <Alert color="red" title="Critical gaps">
            <Stack gap="xs">
              {analysis.critical_gaps.map((gap) => (
                <Text key={gap}>{gap}</Text>
              ))}
            </Stack>
          </Alert>
        )}

        <Stack gap="xs">
          <Text fw={500}>Reasoning</Text>
          <Text>{analysis.reasoning}</Text>
        </Stack>
      </Stack>
    </Paper>
  );
}
