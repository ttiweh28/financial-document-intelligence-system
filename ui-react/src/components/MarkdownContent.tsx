import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type Props = {
  content: string
}

export default function MarkdownContent({ content }: Props) {
  return (
    <div dir="ltr" className="text-left text-sm leading-7 sm:text-[15px]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: (props) => (
            <a
              {...props}
              className="underline underline-offset-2 hover:opacity-90"
              target="_blank"
              rel="noreferrer"
            />
          ),
          code: ({ className, children, ...props }) => (
            <code
              {...props}
              className={`rounded bg-black/5 px-1 py-0.5 font-mono text-[0.95em] ${className ?? ''}`}
            >
              {children}
            </code>
          ),
          pre: ({ children, ...props }) => (
            <pre
              {...props}
              className="mt-2 overflow-x-auto rounded-xl border border-zinc-200 bg-zinc-50 p-3"
            >
              {children}
            </pre>
          ),
          ul: (props) => <ul {...props} className="my-2 list-disc pl-5" />,
          ol: (props) => <ol {...props} className="my-2 list-decimal pl-5" />,
          li: (props) => <li {...props} className="my-1" />,
          p: (props) => <p {...props} className="my-2" />,
          h1: (props) => <h1 {...props} className="my-2 text-base font-semibold" />,
          h2: (props) => <h2 {...props} className="my-2 text-sm font-semibold" />,
          h3: (props) => <h3 {...props} className="my-2 text-sm font-semibold" />,
          blockquote: (props) => (
            <blockquote
              {...props}
              className="my-2 border-l-2 border-zinc-300 pl-3 text-zinc-600"
            />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
