import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon, SparklesIcon } from '@heroicons/react/24/outline'
import ChatMessage from './ChatMessage'
import { useChatStore } from '@/store/chatStore'
import { useChat } from '@/hooks/useChat'

export default function ChatInterface() {
  const [message, setMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { messages } = useChatStore()
  const { sendMessage, isLoading } = useChat()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || isLoading) return

    const userMessage = message.trim()
    setMessage('')
    setIsTyping(true)

    try {
      await sendMessage(userMessage)
    } finally {
      setIsTyping(false)
    }
  }

  const quickCommands = [
    'Provisionar um servidor web com nginx',
    'Criar cluster Kubernetes com 3 nodes',
    'Configurar monitoramento com Prometheus',
    'Fazer backup do banco de dados',
    'Verificar status da infraestrutura',
  ]

  return (
    <div className="flex flex-col h-full">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="glass-card max-w-2xl">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600/20 rounded-full mx-auto mb-4">
                <SparklesIcon className="w-8 h-8 text-primary-400" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">
                Bem-vindo ao ByteShift Orchestrator
              </h2>
              <p className="text-dark-400 mb-6">
                Descreva em linguagem natural o que você quer fazer com sua infraestrutura. 
                Nosso agente de IA irá interpretar, planejar e executar com segurança.
              </p>
              
              <div className="space-y-2">
                <p className="text-sm font-medium text-dark-300 mb-3">Comandos de exemplo:</p>
                {quickCommands.map((command, index) => (
                  <button
                    key={index}
                    onClick={() => setMessage(command)}
                    className="block w-full text-left p-3 rounded-lg bg-dark-700/30 hover:bg-dark-700/50 text-dark-300 hover:text-white transition-all duration-200 text-sm"
                  >
                    "{command}"
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isTyping && (
              <div className="flex items-center space-x-2 text-dark-400">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-sm">IA está pensando...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input form */}
      <div className="border-t border-dark-700/50 p-6">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <div className="flex-1">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Descreva o que você quer fazer com sua infraestrutura..."
              className="input-field w-full resize-none"
              rows={3}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSubmit(e)
                }
              }}
            />
          </div>
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="btn-primary self-end flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="w-4 h-4" />
            <span>Enviar</span>
          </button>
        </form>
        
        <div className="flex items-center justify-between mt-3 text-xs text-dark-500">
          <span>Pressione Enter para enviar, Shift+Enter para nova linha</span>
          <span>Powered by ByteShift AI</span>
        </div>
      </div>
    </div>
  )
}
