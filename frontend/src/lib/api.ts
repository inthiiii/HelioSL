import { getToken } from "./auth";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000/api/v1";

type ApiErrorResponse = {
  detail?: string | Array<{ msg?: string }>;
};

function getErrorMessage(data: ApiErrorResponse): string {
  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (Array.isArray(data.detail)) {
    return data.detail
      .map((item) => item.msg)
      .filter(Boolean)
      .join(", ");
  }

  return "Request failed";
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers = new Headers(options.headers);

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
    }
  );

  if (!response.ok) {
    let message = "Request failed";

    try {
      const data = (await response.json()) as ApiErrorResponse;
      message = getErrorMessage(data);
    } catch {
      // Ignore JSON parse failure.
    }

    throw new Error(message);
  }

  return response.json();
}
