import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { 
  UserIcon, 
  SparklesIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon,
  ClockIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { ChatMessage as ChatMessageType } from '@/types/chat'

interface ChatMessageProps {
  message: ChatMessageType
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.type === 'user'
  const isSystem = message.type === 'system'

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-400 bg-green-900/20'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20'
      case 'high': return 'text-orange-400 bg-orange-900/20'
      case 'critical': return 'text-red-400 bg-red-900/20'
      default: return 'text-dark-400 bg-dark-700/20'
    }
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
      <div className={`max-w-3xl ${isUser ? 'ml-12' : 'mr-12'}`}>
        <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-primary-600' 
              : isSystem 
                ? 'bg-orange-600' 
                : 'bg-gradient-to-br from-purple-500 to-pink-500'
          }`}>
            {isUser ? (
              <UserIcon className="w-4 h-4 text-white" />
            ) : isSystem ? (
              <ExclamationTriangleIcon className="w-4 h-4 text-white" />
            ) : (
              <SparklesIcon className="w-4 h-4 text-white" />
            )}
          </div>

          {/* Message content */}
          <div className={`glass-card ${isUser ? 'bg-primary-900/20' : 'bg-dark-800/40'}`}>
            {/* Header */}
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-dark-300">
                {isUser ? 'Você' : isSystem ? 'Sistema' : 'ByteShift IA'}
              </span>
              <span className="text-xs text-dark-500">
                {format(new Date(message.timestamp), 'HH:mm', { locale: ptBR })}
              </span>
            </div>

            {/* Message text */}
            <div className="text-dark-100 whitespace-pre-wrap mb-3">
              {message.content}
            </div>

            {/* Plan details (for AI responses) */}
            {message.plan && (
              <div className="border-t border-dark-700/50 pt-4 mt-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-sm font-medium text-white">Plano de Execução</h4>
                  <div className="flex items-center space-x-2">
                    {message.risk_level && (
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(message.risk_level)}`}>
                        Risco: {message.risk_level}
                      </span>
                    )}
                    {message.requires_approval && (
                      <span className="px-2 py-1 rounded-full text-xs font-medium text-yellow-400 bg-yellow-900/20">
                        Requer Aprovação
                      </span>
                    )}
                  </div>
                </div>

                {/* Steps */}
                {message.plan.steps && (
                  <div className="space-y-2 mb-4">
                    {message.plan.steps.map((step: any, index: number) => (
                      <div key={index} className="flex items-center space-x-3 p-2 rounded-lg bg-dark-700/30">
                        <div className="flex-shrink-0 w-6 h-6 bg-primary-600/20 rounded-full flex items-center justify-center text-xs text-primary-400 font-medium">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <div className="text-sm text-white font-medium">{step.name}</div>
                          <div className="text-xs text-dark-400">{step.description}</div>
                        </div>
                        <div className="flex items-center space-x-1 text-xs text-dark-500">
                          <ClockIcon className="w-3 h-3" />
                          <span>{step.estimated_time}min</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Estimated duration */}
                {message.estimated_duration && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-dark-400">Duração estimada:</span>
                    <span className="text-white font-medium">{message.estimated_duration} minutos</span>
                  </div>
                )}

                {/* Action buttons */}
                <div className="flex space-x-2 mt-4">
                  {message.requires_approval ? (
                    <>
                      <button className="btn-primary text-sm">
                        <CheckCircleIcon className="w-4 h-4 mr-1" />
                        Aprovar e Executar
                      </button>
                      <button className="btn-secondary text-sm">
                        Modificar Plano
                      </button>
                    </>
                  ) : (
                    <button className="btn-primary text-sm">
                      <PlayIcon className="w-4 h-4 mr-1" />
                      Executar Agora
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
