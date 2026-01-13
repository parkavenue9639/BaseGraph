import { create } from 'zustand'
import { UserResponse } from '../types/auth'
import { login, register, getCurrentUser } from '../services/auth'

interface AuthState {
  user: UserResponse | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string | undefined, email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  login: async (email: string, password: string) => {
    const response = await login({ email, password })
    localStorage.setItem('access_token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
    set({ user: response.user, token: response.access_token, isAuthenticated: true })
  },

  register: async (name: string | undefined, email: string, password: string) => {
    await register({ name, email, password })
    // 注册成功后自动登录
    await useAuthStore.getState().login(email, password)
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    set({ user: null, token: null, isAuthenticated: false })
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const user = await getCurrentUser()
        set({ user, token, isAuthenticated: true })
      } catch (error) {
        useAuthStore.getState().logout()
      }
    }
  },
}))
