export interface User {
  id: number;
  full_name: string;
  email: string;
  district?: string | null;
  user_type: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface UserUpdate {
  full_name?: string;
  district?: string | null;
  user_type?: "household" | "business";
}
