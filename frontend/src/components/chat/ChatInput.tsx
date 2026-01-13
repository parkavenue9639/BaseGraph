import { useState, KeyboardEvent } from 'react'

interface ChatInputProps {
  onSend: (content: string) => void
  onClear: () => void
  disabled?: boolean
}

export default function ChatInput({ onSend, onClear, disabled }: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="border-t border-gray-300/30 bg-white/70 backdrop-blur-md p-4 shadow-lg">
      <div className="flex items-center gap-3 max-w-4xl mx-auto">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
            rows={1}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 bg-gray-50 text-gray-900 placeholder:text-gray-400 shadow-sm"
            style={{ minHeight: '52px', maxHeight: '200px' }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement
              target.style.height = 'auto'
              target.style.height = `${Math.min(target.scrollHeight, 200)}px`
            }}
          />
        </div>
        <div className="flex gap-2 shrink-0">
          <button
            onClick={handleSend}
            disabled={!input.trim() || disabled}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:transform-none flex items-center justify-center min-h-[52px]"
          >
            Send
          </button>
          <button
            onClick={onClear}
            disabled={disabled}
            className="px-4 py-3 bg-gray-100 text-gray-700 font-medium rounded-xl hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow flex items-center justify-center min-h-[52px]"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  )
}
