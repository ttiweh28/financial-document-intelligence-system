import { useState } from 'react'
import type { Chat } from '../types/chat'

type Props = {
  chats: Chat[]
  activeChatId: string
  onSelectChat: (chatId: string) => void
  onDeleteChat: (chatId: string) => void
  onRenameChat: (chatId: string, title: string) => void
  onNewChat: () => void
  onClearAllChats: () => void
  disableNewChat?: boolean
}

export default function ChatSidebar({
  chats,
  activeChatId,
  onSelectChat,
  onDeleteChat,
  onRenameChat,
  onClearAllChats,
}: Props) {
  const [editingChatId, setEditingChatId] = useState<string | null>(null)
  const [editingTitle, setEditingTitle] = useState<string>('')
  const [editingOriginalTitle, setEditingOriginalTitle] = useState<string>('')

  return (
    <aside className="hidden w-72 flex-col border-r border-zinc-200 bg-zinc-50 sm:flex">
      <div className="flex items-center justify-between gap-3 border-b border-zinc-200 px-4 py-6">
        <div className="min-w-0">
          <div className="truncate text-xs text-zinc-500">Select a conversation</div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onClearAllChats}
            className="rounded-xl border border-zinc-200 bg-white px-3 py-2 text-xs font-semibold text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            disabled={chats.length === 0}
            title="Remove all chats"
          >
            Clear all CHATS
          </button>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto p-2">
        {chats.length === 0 ? (
          <div className="px-3 py-4 text-sm text-zinc-500">
            No chats yet. Click <span className="font-medium text-zinc-700">New chat</span> to start.
          </div>
        ) : (
          <div className="flex flex-col gap-1">
            {chats.map((chat) => {
              const isActive = chat.id === activeChatId
              const isEditing = chat.id === editingChatId

              return (
                <div key={chat.id} className="group flex items-stretch gap-1">
                  <button
                    onClick={() => onSelectChat(chat.id)}
                    onDoubleClick={() => {
                      setEditingChatId(chat.id)
                      const current = chat.title || ''
                      setEditingTitle(current)
                      setEditingOriginalTitle(current)
                    }}
                    className={`min-w-0 flex-1 rounded-xl px-3 py-2 text-left text-sm transition ${
                      isActive
                        ? 'bg-white text-zinc-900 shadow-sm ring-1 ring-zinc-200'
                        : 'text-zinc-700 hover:bg-white/70'
                    }`}
                    type="button"
                  >
                    {isEditing ? (
                      <input
                        value={editingTitle}
                        onChange={(e) => {
                          const next = e.target.value
                          setEditingTitle(next)
                          onRenameChat(chat.id, next)
                        }}
                        onBlur={() => setEditingChatId(null)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault()
                            ;(e.currentTarget as HTMLInputElement).blur()
                          }
                          if (e.key === 'Escape') {
                            e.preventDefault()
                            onRenameChat(chat.id, editingOriginalTitle)
                            setEditingTitle(editingOriginalTitle)
                            setEditingChatId(null)
                          }
                        }}
                        autoFocus
                        className="w-full bg-transparent px-0 py-0 text-sm font-medium text-zinc-900 outline-none"
                        aria-label="Chat title"
                      />
                    ) : (
                      <div className="truncate font-medium">{chat.title || 'New chat'}</div>
                    )}
                  </button>

                  <div
                    className={`flex shrink-0 items-center justify-center transition-opacity ${
                      isEditing
                        ? 'opacity-100'
                        : 'pointer-events-none opacity-0 group-hover:pointer-events-auto group-hover:opacity-100 group-focus-within:pointer-events-auto group-focus-within:opacity-100'
                    }`}
                  >
                    <button
                      onClick={() => onDeleteChat(chat.id)}
                      className={`flex items-center justify-center rounded-xl px-2 py-2 text-zinc-500 transition hover:bg-white/70 hover:text-zinc-700 ${
                        isActive ? 'bg-white ring-1 ring-zinc-200' : ''
                      }`}
                      type="button"
                      aria-label="Delete chat"
                      title="Delete chat"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        className="h-4 w-4"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M6 7h12m-1 0-.867 12.142A2 2 0 0 1 14.138 21H9.862a2 2 0 0 1-1.995-1.858L7 7m3 0V5a2 2 0 0 1 2-2h0a2 2 0 0 1 2 2v2"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </nav>
    </aside>
  )
}
