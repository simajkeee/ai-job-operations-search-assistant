import type { ReactNode } from "react";
import { Button, Stack, TextInput, TagsInput, Checkbox } from "@mantine/core";

import type { JobPreferenceInput, WorkMode } from "./types.ts";

type JobPreferenceValidationErrors = {
  targetTitle?: ReactNode;
  keywords?: ReactNode;
  acceptedWorkModes?: ReactNode;
};

type JobPreferenceEditorProps = {
  preference: JobPreferenceInput;
  onChange: (preference: JobPreferenceInput) => void;
  onRemove: () => void;
  onClose?: () => void;
  disabled: boolean;
  validationErrors: JobPreferenceValidationErrors;
};

export function JobPreferenceEditor({
  preference,
  onChange,
  onRemove,
  onClose,
  disabled,
  validationErrors,
}: JobPreferenceEditorProps) {
  return (
    <Stack>
      <TextInput
        label="Target role"
        value={preference.target_title}
        disabled={disabled}
        onChange={(event) => {
          onChange({
            ...preference,
            target_title: event.currentTarget.value,
          });
        }}
        error={validationErrors.targetTitle}
      />

      <TagsInput
        label="Keywords"
        description="Press Enter or comma after each keyword."
        value={preference.keywords}
        disabled={disabled}
        splitChars={[","]}
        onChange={(keywords) => {
          onChange({
            ...preference,
            keywords,
          });
        }}
        error={validationErrors.keywords}
      />

      <Checkbox.Group
        label="Accepted work modes"
        value={preference.accepted_work_modes}
        onChange={(acceptedWorkModes) => {
          onChange({
            ...preference,
            accepted_work_modes: acceptedWorkModes as WorkMode[],
          });
        }}
        error={validationErrors.acceptedWorkModes}
      >
        <Stack mt="xs" gap="xs">
          <Checkbox value="remote" label="Remote" disabled={disabled} />
          <Checkbox value="hybrid" label="Hybrid" disabled={disabled} />
          <Checkbox value="office" label="Office" disabled={disabled} />
        </Stack>
      </Checkbox.Group>

      {onClose !== undefined && (
        <Button
          type="button"
          variant="default"
          disabled={disabled}
          onClick={onClose}
        >
          Done
        </Button>
      )}

      <Button
        type="button"
        color="red"
        variant="light"
        disabled={disabled}
        onClick={onRemove}
      >
        Remove
      </Button>
    </Stack>
  );
}
