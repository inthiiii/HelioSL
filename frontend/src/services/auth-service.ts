import { apiRequest } from "@/lib/api";

import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
} from "@/types/auth";

import type { User } from "@/types/user";


export function registerUser(
  data: RegisterRequest
) {
  return apiRequest<User>(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}


export function loginUser(
  data: LoginRequest
) {
  return apiRequest<TokenResponse>(
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}


export function getCurrentUser() {
  return apiRequest<User>(
    "/auth/me"
  );
}