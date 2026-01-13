import { ChatMessage as ChatMessageType } from '../../types/chat'
import { format } from 'date-fns'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import 'highlight.js/styles/github.css'

interface ChatMessageProps {
  message: ChatMessageType
  timestamp?: Date
}

export default function ChatMessage({ message, timestamp }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6 px-4`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-5 py-4 shadow-md ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white'
            : 'bg-white/95 backdrop-blur-sm text-gray-900 border border-gray-200/50'
        }`}
      >
        {isUser ? (
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
        ) : (
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
              components={{
                // Custom code block styles
                code({ node, inline, className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || '')
                  return !inline && match ? (
                    <pre className="bg-gray-900 border border-gray-800 rounded-xl p-4 overflow-x-auto my-4 shadow-lg">
                      <code className={className} {...props}>
                        {children}
                      </code>
                    </pre>
                  ) : (
                    <code className="bg-gray-100 text-gray-800 px-2 py-1 rounded-md text-sm font-mono border border-gray-200" {...props}>
                      {children}
                    </code>
                  )
                },
                // Custom paragraph styles
                p: ({ children }: any) => <p className="mb-3 last:mb-0 leading-relaxed">{children}</p>,
                // Custom list styles
                ul: ({ children }: any) => <ul className="list-disc mb-3 space-y-2 ml-6">{children}</ul>,
                ol: ({ children }: any) => <ol className="list-decimal mb-3 space-y-2 ml-6">{children}</ol>,
                li: ({ children }: any) => <li className="mb-1 leading-relaxed">{children}</li>,
                // Custom heading styles
                h1: ({ children }: any) => <h1 className="text-3xl font-bold mt-6 mb-4 text-gray-900">{children}</h1>,
                h2: ({ children }: any) => <h2 className="text-2xl font-bold mt-5 mb-3 text-gray-900">{children}</h2>,
                h3: ({ children }: any) => <h3 className="text-xl font-semibold mt-4 mb-3 text-gray-900">{children}</h3>,
                h4: ({ children }: any) => <h4 className="text-lg font-semibold mt-3 mb-2 text-gray-900">{children}</h4>,
                // Custom horizontal rule
                hr: () => <hr className="my-6 border-gray-200" />,
                // Custom blockquote
                blockquote: ({ children }: any) => (
                  <blockquote className="border-l-4 border-blue-500 pl-4 italic my-4 text-gray-700 bg-blue-50 py-2 rounded-r-lg">
                    {children}
                  </blockquote>
                ),
                // Custom table styles
                table: ({ children }: any) => (
                  <div className="overflow-x-auto my-4 rounded-lg border border-gray-200 shadow-sm">
                    <table className="min-w-full border-collapse">
                      {children}
                    </table>
                  </div>
                ),
                thead: ({ children }: any) => <thead className="bg-gray-50">{children}</thead>,
                tbody: ({ children }: any) => <tbody className="bg-white">{children}</tbody>,
                tr: ({ children }: any) => <tr className="border-b border-gray-200 hover:bg-gray-50 transition-colors">{children}</tr>,
                th: ({ children }: any) => <th className="border-b border-gray-200 px-4 py-3 text-left font-semibold text-gray-700">{children}</th>,
                td: ({ children }: any) => <td className="border-b border-gray-100 px-4 py-3 text-gray-600">{children}</td>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        {timestamp && (
          <div className="mt-2 text-xs text-text-secondary">
            {format(timestamp, 'HH:mm')}
          </div>
        )}
      </div>
    </div>
  )
}
