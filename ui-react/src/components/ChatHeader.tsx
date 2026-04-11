type Props = {
  title: string
  onNewChat: () => void
  disableNewChat?: boolean
}

export default function ChatHeader({ title, onNewChat, disableNewChat = false }: Props) {
  return (
    <header className="border-b border-zinc-200 bg-white/90 backdrop-blur sm:px-6">
      <div className="flex items-center justify-between gap-4">
        <div className="min-w-0">
          <h1 className="truncate text-lg font-semibold tracking-tight sm:text-xl">{title}</h1>
        </div>

        <button
          onClick={onNewChat}
          className="rounded-xl border border-zinc-200 bg-white px-4 py-2 text-sm font-medium text-zinc-900 transition hover:border-zinc-300 hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          disabled={disableNewChat}
        >
          New chat
        </button>
      </div>
    </header>
  )
}
