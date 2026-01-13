import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import RegisterForm from '../components/auth/RegisterForm'

export default function RegisterPage() {
  const { isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/chat')
    }
  }, [isAuthenticated, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl mb-4 shadow-lg">
            <span className="text-white font-bold text-2xl">MG</span>
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-2">Create Account</h2>
          <p className="text-gray-500 tracking-normal">Sign up to get started with MyGraph Chat</p>
        </div>
        <RegisterForm />
      </div>
    </div>
  )
}
