import { ReactNode } from 'react'
import Header from './Header'
import { UserResponse } from '../../types/auth'

interface LayoutProps {
  children: ReactNode
  user: UserResponse | null
  onLogout: () => void
}

export default function Layout({ children, user, onLogout }: LayoutProps) {
  return (
    <div className="flex flex-col h-screen">
      <Header user={user} onLogout={onLogout} />
      <main className="flex-1 overflow-hidden">{children}</main>
    </div>
  )
}
