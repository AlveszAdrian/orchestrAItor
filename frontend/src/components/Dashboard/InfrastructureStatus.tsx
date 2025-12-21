import { 
  ServerIcon, 
  CircleStackIcon, 
  CloudIcon,
  ShieldCheckIcon 
} from '@heroicons/react/24/outline'

const infrastructure = [
  {
    name: 'Web Servers',
    count: 8,
    healthy: 7,
    icon: ServerIcon,
    status: 'healthy'
  },
  {
    name: 'Databases',
    count: 3,
    healthy: 3,
    icon: CircleStackIcon,
    status: 'healthy'
  },
  {
    name: 'Load Balancers',
    count: 2,
    healthy: 2,
    icon: CloudIcon,
    status: 'healthy'
  },
  {
    name: 'Security Groups',
    count: 12,
    healthy: 11,
    icon: ShieldCheckIcon,
    status: 'warning'
  }
]

const regions = [
  { name: 'us-east-1', status: 'healthy', latency: '12ms' },
  { name: 'us-west-2', status: 'healthy', latency: '45ms' },
  { name: 'eu-west-1', status: 'warning', latency: '78ms' }
]

export default function InfrastructureStatus() {
  return (
    <div className="space-y-6">
      {/* Infrastructure Overview */}
      <div className="glass-card">
        <h3 className="text-lg font-semibold text-white mb-4">
          Status da Infraestrutura
        </h3>
        
        <div className="space-y-4">
          {infrastructure.map((item, index) => {
            const Icon = item.icon
            const healthPercentage = (item.healthy / item.count) * 100
            
            return (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-dark-700/50 rounded-lg flex items-center justify-center">
                    <Icon className="w-4 h-4 text-dark-400" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">{item.name}</div>
                    <div className="text-xs text-dark-400">
                      {item.healthy}/{item.count} saudáveis
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <div className="w-16 bg-dark-700 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        healthPercentage === 100 ? 'bg-green-500' : 
                        healthPercentage >= 80 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${healthPercentage}%` }}
                    />
                  </div>
                  <span className="text-xs text-dark-400 w-8">
                    {Math.round(healthPercentage)}%
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Regions Status */}
      <div className="glass-card">
        <h3 className="text-lg font-semibold text-white mb-4">
          Status das Regiões
        </h3>
        
        <div className="space-y-3">
          {regions.map((region, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${
                  region.status === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'
                }`} />
                <span className="text-sm text-white font-mono">{region.name}</span>
              </div>
              <div className="text-xs text-dark-400">
                {region.latency}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="glass-card">
        <h3 className="text-lg font-semibold text-white mb-4">
          Ações Rápidas
        </h3>
        
        <div className="space-y-2">
          <button className="w-full text-left p-3 rounded-lg bg-dark-700/30 hover:bg-dark-700/50 transition-colors text-sm text-dark-300 hover:text-white">
            Verificar saúde geral
          </button>
          <button className="w-full text-left p-3 rounded-lg bg-dark-700/30 hover:bg-dark-700/50 transition-colors text-sm text-dark-300 hover:text-white">
            Executar backup completo
          </button>
          <button className="w-full text-left p-3 rounded-lg bg-dark-700/30 hover:bg-dark-700/50 transition-colors text-sm text-dark-300 hover:text-white">
            Atualizar certificados
          </button>
          <button className="w-full text-left p-3 rounded-lg bg-dark-700/30 hover:bg-dark-700/50 transition-colors text-sm text-dark-300 hover:text-white">
            Reiniciar serviços
          </button>
        </div>
      </div>
    </div>
  )
}
