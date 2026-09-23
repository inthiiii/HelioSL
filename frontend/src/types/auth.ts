export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  district?: string;
  user_type?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}