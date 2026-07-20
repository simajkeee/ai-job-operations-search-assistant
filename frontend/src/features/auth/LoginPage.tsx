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
import { isEmail, isNotEmpty, useForm } from "@mantine/form";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "./useAuth.ts";

type LoginFormValues = {
  email: string;
  password: string;
};

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<LoginFormValues>({
    mode: "controlled",
    initialValues: {
      email: "",
      password: "",
    },
    validate: {
      email: isEmail("Enter a valid email address"),
      password: isNotEmpty("Enter your password"),
    },
  });

  async function handleSubmit(values: LoginFormValues) {
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login(values.email, values.password);
      navigate("/preferences", { replace: true });
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof Error ? error.message : "Could not sign in",
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
              <Title order={1}>Sign in</Title>
              <Text c="dimmed" size="sm">
                Continue to your job-search workspace.
              </Text>
            </div>

            {errorMessage !== null && (
              <Alert color="red" title="Could not sign in">
                {errorMessage}
              </Alert>
            )}

            <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
              <Stack>
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
                  autoComplete="current-password"
                  withAsterisk
                  disabled={isSubmitting}
                  {...form.getInputProps("password")}
                />

                <Button type="submit" loading={isSubmitting}>
                  Sign in
                </Button>
              </Stack>
            </form>

            <Text ta="center" size="sm">
              Need an account?{" "}
              <Anchor component={Link} to="/register">
                Create account
              </Anchor>
            </Text>
          </Stack>
        </Paper>
      </Center>
    </main>
  );
}
