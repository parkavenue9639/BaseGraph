import apiClient from './api'
import { RegisterRequest, LoginRequest, TokenResponse, UserResponse } from '../types/auth'

export const register = async (data: RegisterRequest): Promise<UserResponse> => {
  const response = await apiClient.post('/auth/register', data)
  return response.data
}

export const login = async (data: LoginRequest): Promise<TokenResponse> => {
  const response = await apiClient.post('/auth/login', data)
  // 保存 token
  localStorage.setItem('access_token', response.data.access_token)
  localStorage.setItem('user', JSON.stringify(response.data.user))
  return response.data
}

export const getCurrentUser = async (): Promise<UserResponse> => {
  const response = await apiClient.get('/auth/me')
  return response.data
}
