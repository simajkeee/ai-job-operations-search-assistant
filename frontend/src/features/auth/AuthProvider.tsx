import { type ReactNode, useCallback, useEffect, useState } from "react";

import { ApiError } from "../../shared/api/ApiError.ts";
import { getCurrentUser, login as requestLogin } from "./api.ts";
import { AuthContext } from "./authContext.ts";
import type { CurrentUser } from "./types.ts";

const ACCESS_TOKEN_STORAGE_KEY = "access_token";

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [accessToken, setAccessToken] = useState<string | null>(() =>
    sessionStorage.getItem(ACCESS_TOKEN_STORAGE_KEY),
  );
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [isInitializing, setIsInitializing] = useState(
    () => sessionStorage.getItem(ACCESS_TOKEN_STORAGE_KEY) !== null,
  );
  const [initializationError, setInitializationError] = useState<Error | null>(
    null,
  );

  const logout = useCallback(() => {
    sessionStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
    setAccessToken(null);
    setCurrentUser(null);
    setIsInitializing(false);
    setInitializationError(null);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const tokenResponse = await requestLogin(email, password);

    sessionStorage.setItem(
      ACCESS_TOKEN_STORAGE_KEY,
      tokenResponse.access_token,
    );
    setAccessToken(tokenResponse.access_token);
    setInitializationError(null);
    setIsInitializing(true);
  }, []);

  useEffect(() => {
    if (accessToken === null) {
      return;
    }

    let isActive = true;

    getCurrentUser(accessToken)
      .then((user) => {
        if (isActive) {
          setCurrentUser(user);
        }
      })
      .catch((error: unknown) => {
        if (!isActive) {
          return;
        }

        if (error instanceof ApiError && error.status === 401) {
          logout();
          return;
        }

        setInitializationError(toError(error));
      })
      .finally(() => {
        if (isActive) {
          setIsInitializing(false);
        }
      });

    return () => {
      isActive = false;
    };
  }, [accessToken, logout]);

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        currentUser,
        isInitializing,
        initializationError,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

function toError(error: unknown): Error {
  if (error instanceof Error) {
    return error;
  }

  return new Error("Could not restore the current session");
}
