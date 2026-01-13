import { useEffect, useRef } from 'react'
import { useChatStore } from '../store/chatStore'
import { useAuthStore } from '../store/authStore'
import MessageList from '../components/chat/MessageList'
import ChatInput from '../components/chat/ChatInput'
import Layout from '../components/layout/Layout'

export default function ChatPage() {
  const { messages, isLoading, sendChatMessage, clearMessages } = useChatStore()
  const { user, logout } = useAuthStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (content: string) => {
    await sendChatMessage(content)
  }

  return (
    <Layout user={user} onLogout={logout}>
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto">
            <MessageList messages={messages} isLoading={isLoading} />
            <div ref={messagesEndRef} />
          </div>
        </div>

        <ChatInput
          onSend={handleSend}
          onClear={clearMessages}
          disabled={isLoading}
        />
      </div>
    </Layout>
  )
}
