import { ApiError } from "./ApiError.ts";

type RequestOptions = RequestInit & {
  accessToken?: string;
};

export async function request<T>(
  path: string,
  { accessToken, headers, ...options }: RequestOptions = {},
): Promise<T> {
  const requestHeaders = new Headers(headers);

  requestHeaders.set("Accept", "application/json");

  if (accessToken) {
    requestHeaders.set("Authorization", `Bearer ${accessToken}`);
  }

  const response = await fetch(path, {
    ...options,
    headers: requestHeaders,
  });

  const body: unknown = await response.json().catch(() => undefined);

  if (!response.ok) {
    throw new ApiError(
      response.status,
      getErrorMessage(body, response.statusText),
      body,
    );
  }

  return body as T;
}

function getErrorMessage(body: unknown, fallback: string): string {
  if (
    typeof body === "object" &&
    body !== null &&
    "detail" in body &&
    typeof body.detail === "string"
  ) {
    return body.detail;
  }

  return fallback || "Request failed";
}
