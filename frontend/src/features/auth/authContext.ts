import { createContext } from "react";

import type { CurrentUser } from "./types.ts";

export type AuthContextValue = {
  accessToken: string | null;
  currentUser: CurrentUser | null;
  isInitializing: boolean;
  initializationError: Error | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextValue | null>(null);
