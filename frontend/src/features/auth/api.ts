import { request } from '../../shared/api/httpClient.ts'

import type {
  AccessTokenResponse,
  CurrentUser,
  RegisteredUser,
  RegisterUserRequest,
} from "./types.ts";

const AUTH_API_PATH = "/api/v1/auth";

export function register(data: RegisterUserRequest): Promise<RegisteredUser> {
  return request<RegisteredUser>(`${AUTH_API_PATH}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

export function login(
  email: string,
  password: string,
): Promise<AccessTokenResponse> {
  const body = new URLSearchParams({
    username: email,
    password,
  });

  return request<AccessTokenResponse>(`${AUTH_API_PATH}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
}

export function getCurrentUser(accessToken: string): Promise<CurrentUser> {
  return request<CurrentUser>(`${AUTH_API_PATH}/me`, {
    accessToken,
  });
}
