export interface UserResponse {
  id: number
  name: string
  email: string
  created_at: string
  updated_at: string
}

export interface RegisterRequest {
  name?: string
  email: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserResponse
}
