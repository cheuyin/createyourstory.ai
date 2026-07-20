export const BASE_URL = import.meta.env.VITE_BASE_URL || "";

export class ApiError extends Error {
  readonly status: number;
  readonly code?: string;

  constructor(
    message: string,
    status: number,
    code?: string,
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

async function readResponseBody(response: Response): Promise<unknown> {
  const body = await response.text();
  if (!body) return null;

  try {
    return JSON.parse(body);
  } catch {
    return body;
  }
}

export async function apiFetch<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(input, init);
  } catch {
    throw new Error("We couldn’t reach the server. Please try again.");
  }

  let data: unknown;
  try {
    data = await readResponseBody(response);
  } catch {
    throw new Error("The server returned an unreadable response. Please try again.");
  }

  if (!response.ok) {
    const errorData = data as
      | { message?: string; error?: string }
      | null;
    const message =
      errorData?.message ||
      errorData?.error ||
      "Something went wrong. Please try again.";
    throw new ApiError(message, response.status, errorData?.error);
  }

  return data as T;
}
