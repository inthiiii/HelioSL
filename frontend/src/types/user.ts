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