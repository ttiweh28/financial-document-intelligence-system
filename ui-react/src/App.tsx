import { useEffect, useMemo, useRef, useState } from 'react'
import ChatComposer from './components/ChatComposer'
import ChatHeader from './components/ChatHeader'
import ChatSidebar from './components/ChatSidebar'
import MessageBubble from './components/MessageBubble'
import type { Chat } from './types/chat'

export default function App() {
  const storageChatsKey = 'fdi_chats'
  const storageActiveChatKey = 'fdi_active_chat_id'

  function generateUserId() {
    if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
      return crypto.randomUUID()
    }

    return `${Date.now()}-${Math.random().toString(16).slice(2)}`
  }

  function createChat() {
    const now = new Date()
    const time = now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
    const userId = generateUserId()

    const newChat: Chat = {
      id: userId,
      title: '',
      userId,
      documentUploaded: false,
      messages: [
        {
          id: `m-${now.getTime()}`,
          role: 'assistant',
          content: 'Upload a file and ask a question about it.',
          time,
        },
      ],
    }

    return newChat
  }

  const [chats, setChats] = useState<Chat[]>(() => {
    if (typeof window === 'undefined') return []
    const raw = window.localStorage.getItem(storageChatsKey)
    if (!raw) return [createChat()]

    try {
      const parsed = JSON.parse(raw) as unknown
      if (!Array.isArray(parsed)) return []
      if (parsed.length === 0) return [createChat()]
      return parsed as Chat[]
    } catch {
      return []
    }
  })

  const [activeChatId, setActiveChatId] = useState<string>(() => {
    if (typeof window === 'undefined') return ''
    const saved = window.localStorage.getItem(storageActiveChatKey)
    return saved ?? ''
  })

  useEffect(() => {
    if (typeof window === 'undefined') return
    window.localStorage.setItem(storageChatsKey, JSON.stringify(chats))
  }, [chats])

  const resolvedActiveChatId = useMemo(() => {
    if (!activeChatId) return chats[0]?.id ?? ''
    if (chats.some((c) => c.id === activeChatId)) return activeChatId
    return chats[0]?.id ?? ''
  }, [activeChatId, chats])

  useEffect(() => {
    if (typeof window === 'undefined') return
    window.localStorage.setItem(storageActiveChatKey, resolvedActiveChatId)
  }, [resolvedActiveChatId])

  const activeChat = useMemo(
    () => chats.find((c) => c.id === resolvedActiveChatId) ?? chats[0],
    [chats, resolvedActiveChatId],
  )

  const messages = activeChat?.messages ?? []

  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [resolvedActiveChatId, messages.length])

  const canCreateNewChat = chats.length === 0 ? true : Boolean(chats[0]?.title)

  function appendMessageToChat(chatId: string, message: Chat['messages'][number]) {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat
        return { ...chat, messages: [...chat.messages, message] }
      }),
    )
  }

  function setChatUserId(chatId: string, userId: string) {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat
        return { ...chat, userId }
      }),
    )
  }

  function setChatTitle(chatId: string, title: string) {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat
        return { ...chat, title }
      }),
    )
  }

  function setChatDocumentUploaded(chatId: string, documentUploaded: boolean) {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat
        return { ...chat, documentUploaded }
      }),
    )
  }

  async function uploadDocument(file: File, userId: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('user_id', userId)

    const res = await fetch('http://127.0.0.1:8000/process-document', {
      method: 'POST',
      headers: {
        accept: 'application/json',
      },
      body: formData,
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(text || `Upload failed (${res.status})`)
    }

    const contentType = res.headers.get('content-type') ?? ''
    if (contentType.includes('application/json')) return (await res.json()) as unknown
    return await res.text()
  }

  async function askFollowUp(question: string, userId: string) {
    const url = new URL('http://127.0.0.1:8000/follow-up')
    url.searchParams.set('user_id', userId)
    url.searchParams.set('question', question)

    const res = await fetch(url.toString(), { method: 'POST' })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(text || `Question failed (${res.status})`)
    }

    const contentType = res.headers.get('content-type') ?? ''
    if (contentType.includes('application/json')) return (await res.json()) as unknown
    return await res.text()
  }

  async function handleSubmit({
    file,
    question,
    setPhase,
  }: {
    file: File | null
    question: string
    setPhase: (phase: 'idle' | 'uploading' | 'thinking') => void
  }) {
    if (!activeChat) return
    if (!activeChat.documentUploaded && !file) return

    const now = new Date()
    const time = now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
    const chatId = activeChat.id

    const userId = activeChat.userId ?? generateUserId()
    if (!activeChat.userId) {
      setChatUserId(chatId, userId)
    }

    if (!activeChat.title) {
      setChatTitle(chatId, question)
    }

    appendMessageToChat(chatId, {
      id: `u-${now.getTime()}`,
      role: 'user',
      content: question,
      time,
    })

    function formatAssistantContent(answer: unknown) {
      if (typeof answer === 'string') return answer

      if (answer && typeof answer === 'object') {
        const parsedDocument = (answer as { parsed_document?: unknown }).parsed_document
        if (parsedDocument && typeof parsedDocument === 'object') {
          const rawText = (parsedDocument as { raw_text?: unknown }).raw_text
          if (typeof rawText === 'string') {
            const trimmed = rawText.trim()
            if (trimmed.length > 0) return trimmed
          }
        }

        const summary = (answer as { summary?: unknown }).summary
        if (typeof summary === 'string' && summary.trim().length > 0) {
          return summary.trim()
        }

        return `\`\`\`json\n${JSON.stringify(answer, null, 2)}\n\`\`\``
      }

      return String(answer)
    }

    try {
      if (!activeChat.documentUploaded) {
        if (!file) return
        setPhase('uploading')
        await uploadDocument(file, userId)
        setChatDocumentUploaded(chatId, true)

        appendMessageToChat(chatId, {
          id: `u-${now.getTime()}-uploaded`,
          role: 'assistant',
          content: 'File uploaded and processing started. Please wait a moment.',
          time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }),
        })
      }

      setPhase('thinking')
      const answer = await askFollowUp(question, userId)

      appendMessageToChat(chatId, {
        id: `a-${now.getTime() + 1}`,
        role: 'assistant',
        content: formatAssistantContent(answer),
        time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }),
      })
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      console.log(message)
      appendMessageToChat(chatId, {
        id: `e-${now.getTime() + 2}`,
        role: 'assistant',
        content: `**${JSON.parse(message).detail}**`,
        time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }),
      })
    }
  }

  function handleNewChat() {
    if (!canCreateNewChat) return
    const newChat = createChat()
    setChats((prev) => [newChat, ...prev])
    setActiveChatId(newChat.id)
  }

  function handleDeleteChat(chatId: string) {
    setChats((prev) => {
      const remaining = prev.filter((c) => c.id !== chatId)
      const nextChats = remaining.length === 0 ? [createChat()] : remaining

      setActiveChatId((prevActive) => {
        if (prevActive !== chatId) return prevActive
        return nextChats[0]?.id ?? ''
      })

      return nextChats
    })
  }

  function handleRenameChat(chatId: string, title: string) {
    setChatTitle(chatId, title.trim())
  }

  function handleClearAllChats() {
    const newChat = createChat()
    setChats([newChat])
    setActiveChatId(newChat.id)
  }

  return (
    <div dir="ltr" className="min-h-screen bg-white text-zinc-900">
      <div className="mx-auto flex h-screen max-w-6xl">
        <ChatSidebar
          chats={chats}
          activeChatId={activeChatId}
          onSelectChat={setActiveChatId}
          onDeleteChat={handleDeleteChat}
          onRenameChat={handleRenameChat}
          onNewChat={handleNewChat}
          onClearAllChats={handleClearAllChats}
          disableNewChat={!canCreateNewChat}
        />

        <div className="flex min-w-0 flex-1 flex-col">
          <ChatHeader
            title="Financial Document Intelligence System"
            onNewChat={handleNewChat}
            disableNewChat={!canCreateNewChat}
          />

          <main className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
            <div className="mx-auto flex w-full max-w-3xl flex-col gap-6">
              {messages.map((message) => {
                return <MessageBubble key={message.id} message={message} />
              })}
              <div ref={bottomRef} />
            </div>
          </main>

          <ChatComposer
            key={resolvedActiveChatId}
            onSubmit={handleSubmit}
            requireFile={!activeChat?.documentUploaded}
            showUpload={!activeChat?.documentUploaded}
          />
        </div>
      </div>
    </div>
  );
}
