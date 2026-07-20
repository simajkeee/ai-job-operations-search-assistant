import {
  Alert,
  Anchor,
  Button,
  Center,
  Paper,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { hasLength, isEmail, useForm } from "@mantine/form";
import { useState } from "react";
import { Link } from "react-router-dom";

import { register } from "./api.ts";

type RegisterFormValues = {
  email: string;
  password: string;
};

export function RegisterPage() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [registeredEmail, setRegisteredEmail] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<RegisterFormValues>({
    mode: "controlled",
    initialValues: {
      email: "",
      password: "",
    },
    validate: {
      email: isEmail("Enter a valid email address"),
      password: hasLength(
        { min: 8, max: 128 },
        "Password must be between 8 and 128 characters",
      ),
    },
  });

  async function handleSubmit(values: RegisterFormValues) {
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await register(values);
      setRegisteredEmail(values.email);
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof Error ? error.message : "Could not create account",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main>
      <Center mih="100dvh" px="md">
        <Paper withBorder shadow="sm" radius="md" p="xl" w="100%" maw={420}>
          <Stack>
            <div>
              <Title order={1}>Create account</Title>
              <Text c="dimmed" size="sm">
                Set up your job-search workspace.
              </Text>
            </div>

            {registeredEmail !== null ? (
              <>
                <Alert color="green" title="Account created">
                  You can now sign in as {registeredEmail}.
                </Alert>

                <Button component={Link} to="/login">
                  Sign in
                </Button>
              </>
            ) : (
              <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
                <Stack>
                  {errorMessage !== null && (
                    <Alert color="red" title="Could not create account">
                      {errorMessage}
                    </Alert>
                  )}

                  <TextInput
                    label="Email"
                    type="email"
                    autoComplete="email"
                    withAsterisk
                    disabled={isSubmitting}
                    {...form.getInputProps("email")}
                  />

                  <PasswordInput
                    label="Password"
                    description="Use 8 to 128 characters."
                    autoComplete="new-password"
                    withAsterisk
                    disabled={isSubmitting}
                    {...form.getInputProps("password")}
                  />

                  <Button type="submit" loading={isSubmitting}>
                    Create account
                  </Button>
                </Stack>
              </form>
            )}

            <Text ta="center" size="sm">
              Already have an account?{" "}
              <Anchor component={Link} to="/login">
                Sign in
              </Anchor>
            </Text>
          </Stack>
        </Paper>
      </Center>
    </main>
  );
}
