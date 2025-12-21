import { useState } from 'react'
import Head from 'next/head'
import Layout from '@/components/Layout'
import ChatInterface from '@/components/Chat/ChatInterface'
import Dashboard from '@/components/Dashboard/Dashboard'
import { useAuthStore } from '@/store/authStore'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'dashboard'>('chat')
  const { isAuthenticated } = useAuthStore()

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-card max-w-md w-full mx-4">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gradient mb-2">
              ByteShift Orchestrator
            </h1>
            <p className="text-dark-400">
              Agente Autônomo de Infraestrutura
            </p>
          </div>
          
          <div className="space-y-4">
            <button
              onClick={() => useAuthStore.getState().login('demo', 'demo')}
              className="w-full btn-primary"
            >
              Entrar como Demo
            </button>
            <p className="text-xs text-dark-500 text-center">
              Use qualquer credencial para acessar o demo
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>ByteShift Orchestrator - Agente de Infraestrutura</title>
        <meta 
          name="description" 
          content="Sistema de IA para automação segura de infraestrutura" 
        />
      </Head>

      <Layout>
        <div className="flex-1 flex flex-col">
          {/* Header com tabs */}
          <div className="glass-effect border-b border-dark-700/50 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex space-x-1">
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    activeTab === 'chat'
                      ? 'bg-primary-600 text-white'
                      : 'text-dark-400 hover:text-dark-200 hover:bg-dark-700/50'
                  }`}
                >
                  Chat IA
                </button>
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    activeTab === 'dashboard'
                      ? 'bg-primary-600 text-white'
                      : 'text-dark-400 hover:text-dark-200 hover:bg-dark-700/50'
                  }`}
                >
                  Dashboard
                </button>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse-slow"></div>
                  <span className="text-sm text-dark-400">Sistema Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Conteúdo principal */}
          <div className="flex-1 overflow-hidden">
            {activeTab === 'chat' && <ChatInterface />}
            {activeTab === 'dashboard' && <Dashboard />}
          </div>
        </div>
      </Layout>
    </>
  )
}
