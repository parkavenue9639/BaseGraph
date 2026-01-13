export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  messages: ChatMessage[]
}

export type SSEEventType = 'user_message' | 'LangGraph' | 'ChatOpenAI' | 'completed'

export interface SSEEvent {
  event: SSEEventType
  data: any
}
