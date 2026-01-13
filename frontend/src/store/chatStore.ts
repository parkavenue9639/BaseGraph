import { create } from 'zustand'
import { ChatMessage } from '../types/chat'
import { sendMessage } from '../services/chat'

interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  error: string | null
  addMessage: (message: ChatMessage) => void
  appendToLastMessage: (content: string) => void
  clearMessages: () => void
  sendChatMessage: (content: string) => Promise<void>
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,

  addMessage: (message: ChatMessage) => {
    set((state) => ({ messages: [...state.messages, message] }))
  },

  appendToLastMessage: (content: string) => {
    set((state) => {
      const messages = [...state.messages]
      const lastMessage = messages[messages.length - 1]
      if (lastMessage && lastMessage.role === 'assistant') {
        lastMessage.content += content
      } else {
        messages.push({ role: 'assistant', content })
      }
      return { messages }
    })
  },

  clearMessages: () => {
    set({ messages: [], error: null })
  },

  sendChatMessage: async (content: string) => {
    const { messages, addMessage, appendToLastMessage } = get()

    // 添加用户消息
    const userMessage: ChatMessage = { role: 'user', content }
    addMessage(userMessage)

    // 添加空的 AI 消息占位
    addMessage({ role: 'assistant', content: '' })

    set({ isLoading: true, error: null })

    try {
      await sendMessage(
        [...messages, userMessage],
        (chunk) => {
          appendToLastMessage(chunk)
        },
        () => {
          set({ isLoading: false })
        },
        (error) => {
          set({ isLoading: false, error: error.message })
        }
      )
    } catch (error) {
      set({ isLoading: false, error: (error as Error).message })
    }
  },
}))
