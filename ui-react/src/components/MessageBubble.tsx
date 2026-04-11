import type { Message } from '../types/chat'
import MarkdownContent from './MarkdownContent'

type Props = {
  message: Message
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-sm ${
          isUser
            ? 'bg-emerald-600 text-white'
            : 'border border-zinc-200 bg-white text-zinc-900'
        }`}
      >
        <div className="mb-1 flex items-center gap-2">
          <span
            className={`text-xs font-semibold uppercase tracking-wide ${
              isUser ? 'text-white/80' : 'text-zinc-500'
            }`}
          >
            {isUser ? 'You' : 'Assistant'}
          </span>
          <span className={`text-xs ${isUser ? 'text-white/70' : 'text-zinc-400'}`}>{message.time}</span>
        </div>

        <MarkdownContent content={message.content} />
      </div>
    </div>
  )
}
