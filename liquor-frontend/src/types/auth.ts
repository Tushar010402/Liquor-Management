export type UserRole = 'saas_admin' | 'tenant_admin' | 'manager' | 'assistant_manager' | 'executive';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  tenant_id?: string;
  assigned_shops?: { id: string; name: string }[];
  permissions?: string[];
}

export interface UserRegistrationData {
  email: string;
  password: string;
  full_name: string;
  role?: UserRole;
  tenant_id?: string;
} 