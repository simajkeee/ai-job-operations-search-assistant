import { AppShell, Button, Group, Text, Title } from "@mantine/core";
import { Link, Outlet } from "react-router-dom";

import { useAuth } from "../features/auth/useAuth.ts";

export function AppLayout() {
  const { currentUser, logout } = useAuth();

  return (
    <AppShell header={{ height: 64 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group gap="xs">
            <Title order={3}>Job Search Assistant</Title>

            <Button component={Link} to="/preferences" variant="subtle">
              Preferences
            </Button>

            <Button component={Link} to="/analyze" variant="subtle">
              Analyze vacancy
            </Button>
          </Group>

          <Group gap="sm">
            {currentUser !== null && (
              <Text c="dimmed" size="sm">
                {currentUser.email}
              </Text>
            )}

            <Button color="gray" variant="light" onClick={logout}>
              Sign out
            </Button>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
