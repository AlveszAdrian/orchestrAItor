import { 
  ClockIcon, 
  CheckCircleIcon, 
  ExclamationCircleIcon,
  PlayIcon 
} from '@heroicons/react/24/outline'

const tasks = [
  {
    id: 1,
    title: 'Provisionar servidor web',
    description: 'Criar instância EC2 com nginx configurado',
    status: 'pending',
    priority: 'high',
    estimatedTime: 30,
    createdAt: '2024-01-01T10:00:00Z'
  },
  {
    id: 2,
    title: 'Backup banco de dados',
    description: 'Backup automático do PostgreSQL principal',
    status: 'executing',
    priority: 'medium',
    estimatedTime: 45,
    createdAt: '2024-01-01T09:30:00Z'
  },
  {
    id: 3,
    title: 'Atualizar certificados SSL',
    description: 'Renovar certificados que expiram em 7 dias',
    status: 'completed',
    priority: 'high',
    estimatedTime: 15,
    createdAt: '2024-01-01T08:00:00Z'
  },
  {
    id: 4,
    title: 'Configurar monitoramento',
    description: 'Instalar Prometheus nos novos servidores',
    status: 'failed',
    priority: 'medium',
    estimatedTime: 60,
    createdAt: '2024-01-01T07:00:00Z'
  }
]

const statusConfig = {
  pending: {
    icon: ClockIcon,
    color: 'text-yellow-400 bg-yellow-900/20',
    label: 'Pendente'
  },
  executing: {
    icon: PlayIcon,
    color: 'text-blue-400 bg-blue-900/20',
    label: 'Executando'
  },
  completed: {
    icon: CheckCircleIcon,
    color: 'text-green-400 bg-green-900/20',
    label: 'Concluída'
  },
  failed: {
    icon: ExclamationCircleIcon,
    color: 'text-red-400 bg-red-900/20',
    label: 'Falhou'
  }
}

const priorityColors = {
  low: 'border-l-green-500',
  medium: 'border-l-yellow-500',
  high: 'border-l-red-500'
}

export default function TasksList() {
  return (
    <div className="glass-card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">
          Tarefas Recentes
        </h3>
        <button className="text-sm text-primary-400 hover:text-primary-300">
          Ver todas
        </button>
      </div>

      <div className="space-y-4">
        {tasks.map((task) => {
          const status = statusConfig[task.status as keyof typeof statusConfig]
          const Icon = status.icon

          return (
            <div 
              key={task.id}
              className={`p-4 rounded-lg bg-dark-700/30 border-l-4 ${priorityColors[task.priority as keyof typeof priorityColors]} hover:bg-dark-700/50 transition-colors cursor-pointer`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h4 className="font-medium text-white">{task.title}</h4>
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${status.color}`}>
                      <Icon className="w-3 h-3 mr-1" />
                      {status.label}
                    </span>
                  </div>
                  <p className="text-sm text-dark-400 mb-2">{task.description}</p>
                  <div className="flex items-center space-x-4 text-xs text-dark-500">
                    <span>Duração: {task.estimatedTime}min</span>
                    <span>Prioridade: {task.priority}</span>
                  </div>
                </div>
                
                {task.status === 'pending' && (
                  <button className="btn-primary text-xs">
                    Executar
                  </button>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
