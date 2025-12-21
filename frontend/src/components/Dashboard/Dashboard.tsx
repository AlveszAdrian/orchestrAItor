import { 
  ServerIcon, 
  ChartBarIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline'
import MetricCard from './MetricCard'
import TasksList from './TasksList'
import InfrastructureStatus from './InfrastructureStatus'

export default function Dashboard() {
  const metrics = [
    {
      title: 'Servidores Ativos',
      value: '24',
      change: '+2',
      changeType: 'increase' as const,
      icon: ServerIcon,
      color: 'blue'
    },
    {
      title: 'Tarefas Pendentes',
      value: '8',
      change: '-3',
      changeType: 'decrease' as const,
      icon: ClockIcon,
      color: 'yellow'
    },
    {
      title: 'Alertas Críticos',
      value: '2',
      change: '+1',
      changeType: 'increase' as const,
      icon: ExclamationTriangleIcon,
      color: 'red'
    },
    {
      title: 'Taxa de Sucesso',
      value: '98.5%',
      change: '+0.3%',
      changeType: 'increase' as const,
      icon: CheckCircleIcon,
      color: 'green'
    }
  ]

  return (
    <div className="p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-dark-400 mt-1">
            Visão geral da sua infraestrutura e operações
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary">
            <ChartBarIcon className="w-4 h-4 mr-2" />
            Relatórios
          </button>
          <button className="btn-primary">
            <CpuChipIcon className="w-4 h-4 mr-2" />
            Nova Tarefa
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tasks List */}
        <div className="lg:col-span-2">
          <TasksList />
        </div>

        {/* Infrastructure Status */}
        <div className="lg:col-span-1">
          <InfrastructureStatus />
        </div>
      </div>

      {/* System Health */}
      <div className="glass-card">
        <h3 className="text-lg font-semibold text-white mb-4">
          Saúde do Sistema
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
              <div className="w-8 h-8 bg-green-500 rounded-full"></div>
            </div>
            <div className="text-sm font-medium text-white">API Gateway</div>
            <div className="text-xs text-green-400">Online</div>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
              <div className="w-8 h-8 bg-green-500 rounded-full"></div>
            </div>
            <div className="text-sm font-medium text-white">Banco de Dados</div>
            <div className="text-xs text-green-400">Conectado</div>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
              <div className="w-8 h-8 bg-yellow-500 rounded-full"></div>
            </div>
            <div className="text-sm font-medium text-white">Executor</div>
            <div className="text-xs text-yellow-400">Ocupado</div>
          </div>
        </div>
      </div>
    </div>
  )
}
