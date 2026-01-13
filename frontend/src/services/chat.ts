import { ChatMessage } from '../types/chat'
import { API_BASE_URL } from '../utils/constants'
import { createSSEConnection } from '../utils/sse'

const getToken = (): string | null => {
  return localStorage.getItem('access_token')
}

export const sendMessage = async (
  messages: ChatMessage[],
  onMessage: (content: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): Promise<() => void> => {
  const token = getToken()
  if (!token) {
    throw new Error('Not authenticated')
  }

  const abort = createSSEConnection(
    `${API_BASE_URL}/chat/stream`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: { messages },
      onMessage: (event, data) => {
        // Handle ChatOpenAI event content
        if (event === 'ChatOpenAI' && data.chunk?.content) {
          onMessage(data.chunk.content)
        }
      },
      onComplete,
      onError,
    }
  )

  return abort
}
