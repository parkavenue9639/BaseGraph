import { UserResponse } from '../../types/auth'

interface HeaderProps {
  user: UserResponse | null
  onLogout: () => void
}

export default function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="bg-white/70 backdrop-blur-md border-b border-gray-300/30 px-6 py-4 flex items-center justify-between shadow-sm sticky top-0 z-10">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-sm">MG</span>
        </div>
        <h1 className="text-xl font-semibold tracking-tight bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
          MyGraph Chat
        </h1>
      </div>
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-50 rounded-full">
            <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-xs font-medium">
                {(user.name || user.email)[0].toUpperCase()}
              </span>
            </div>
            <span className="text-sm font-medium tracking-tight text-gray-700">
              {user.name || user.email.split('@')[0]}
            </span>
          </div>
        )}
        <button
          onClick={onLogout}
          className="px-4 py-2 text-sm font-medium tracking-tight text-gray-700 hover:bg-gray-100 rounded-lg transition-all duration-200 hover:shadow-sm"
        >
          Sign Out
        </button>
      </div>
    </header>
  )
}
