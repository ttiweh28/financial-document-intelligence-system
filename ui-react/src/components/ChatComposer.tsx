import { useRef, useState } from 'react'

type SubmitPhase = 'idle' | 'uploading' | 'thinking'

type Props = {
  placeholder?: string
  onSubmit: (args: {
    file: File | null
    question: string
    setPhase: (phase: SubmitPhase) => void
  }) => Promise<void>
  requireFile?: boolean
  showUpload?: boolean
}

export default function ChatComposer({
  placeholder = 'Ask a question about your file...',
  onSubmit,
  requireFile = true,
  showUpload = true,
}: Props) {
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [question, setQuestion] = useState<string>('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [phase, setPhase] = useState<SubmitPhase>('idle')

  async function handleSubmit() {
    if (isSubmitting) return
    const trimmed = question.trim()
    if ((requireFile && !file) || !trimmed) return

    try {
      setIsSubmitting(true)
      setPhase(requireFile ? 'uploading' : 'thinking')
      await onSubmit({ file, question: trimmed, setPhase })
      setQuestion('')
    } finally {
      setIsSubmitting(false)
      setPhase('idle')
    }
  }

  return (
    <footer className="border-t border-zinc-200 bg-white px-4 py-4 sm:px-6">
      <div className="mx-auto w-full max-w-3xl">
        <div className="rounded-3xl border border-zinc-200 bg-white p-3 shadow-2xl">
          <div className="mb-3 flex flex-wrap items-center gap-3">
            {showUpload ? (
              <>
                <button
                  className="inline-flex cursor-pointer items-center gap-2 rounded-xl border border-dashed border-zinc-300 bg-white px-4 py-2 text-sm text-zinc-700 transition hover:border-zinc-400 hover:bg-zinc-50"
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isSubmitting}
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
                      d="M12 16V4m0 0-4 4m4-4 4 4M4 16.5v1.75A1.75 1.75 0 0 0 5.75 20h12.5A1.75 1.75 0 0 0 20 18.25V16.5"
                    />
                  </svg>
                  <span>Upload file</span>
                </button>

                <input
                  ref={fileInputRef}
                  type="file"
                  className="hidden"
                  onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                />

                <div className="rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-500">
                  {file ? file.name : 'No file selected'}
                </div>
              </>
            ) : null}
          </div>

          <div className="flex flex-col gap-3">
            <textarea
              rows={4}
              placeholder={placeholder}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full resize-none rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-900 outline-none placeholder:text-zinc-400 focus:border-zinc-300 sm:text-[15px]"
              disabled={isSubmitting}
            />

            <div className="flex items-center justify-between gap-3">
              <p className="text-xs text-zinc-500 sm:text-sm">It’s better to upload the PDF file.</p>

              <button
                className="inline-flex items-center gap-2 rounded-2xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
                type="button"
                onClick={handleSubmit}
                disabled={
                  isSubmitting ||
                  (requireFile && !file) ||
                  question.trim().length === 0
                }
              >
                {isSubmitting ? (
                  <svg
                    className="h-4 w-4 animate-spin"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="3"
                    />
                    <path
                      className="opacity-75"
                      d="M22 12a10 10 0 0 1-10 10"
                      stroke="currentColor"
                      strokeWidth="3"
                      strokeLinecap="round"
                    />
                  </svg>
                ) : null}
                {phase === 'uploading'
                  ? 'Uploading file ...'
                  : phase === 'thinking'
                    ? 'Thinking ...'
                    : 'Submit'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
