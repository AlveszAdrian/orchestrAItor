import { useState } from 'react'
import { 
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  ServerIcon,
  CogIcon,
  DocumentTextIcon,
  ShieldCheckIcon,
  BellIcon,
  UserIcon
} from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Chat IA', icon: ChatBubbleLeftRightIcon, href: '#', current: true },
  { name: 'Dashboard', icon: ChartBarIcon, href: '#', current: false },
  { name: 'Infraestrutura', icon: ServerIcon, href: '#', current: false },
  { name: 'Tarefas', icon: DocumentTextIcon, href: '#', current: false },
  { name: 'Governança', icon: ShieldCheckIcon, href: '#', current: false },
  { name: 'Alertas', icon: BellIcon, href: '#', current: false },
  { name: 'Configurações', icon: CogIcon, href: '#', current: false },
]

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div className={`${collapsed ? 'w-16' : 'w-64'} transition-all duration-300 glass-effect border-r border-dark-700/50 flex flex-col`}>
      {/* Logo */}
      <div className="flex items-center justify-between p-4 border-b border-dark-700/50">
        {!collapsed && (
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">BS</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">ByteShift</h1>
              <p className="text-xs text-dark-400">Orchestrator</p>
            </div>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-lg hover:bg-dark-700/50 transition-colors"
        >
          <svg 
            className={`w-5 h-5 text-dark-400 transition-transform ${collapsed ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navigation.map((item) => {
          const Icon = item.icon
          return (
            <a
              key={item.name}
              href={item.href}
              className={`sidebar-item ${item.current ? 'active' : ''}`}
              title={collapsed ? item.name : undefined}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && (
                <span className="ml-3 text-sm font-medium">{item.name}</span>
              )}
            </a>
          )
        })}
      </nav>

      {/* User section */}
      <div className="border-t border-dark-700/50 p-3">
        <div className={`flex items-center ${collapsed ? 'justify-center' : 'space-x-3'} p-2 rounded-lg hover:bg-dark-700/50 transition-colors cursor-pointer`}>
          <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
            <UserIcon className="w-4 h-4 text-white" />
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">Admin</p>
              <p className="text-xs text-dark-400 truncate">admin@byteshift.com</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
