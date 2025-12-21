import { useState } from 'react'
import { useChatStore } from '@/store/chatStore'
import { useAuthStore } from '@/store/authStore'
import { ChatResponse } from '@/types/chat'
import toast from 'react-hot-toast'

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)
  const { addMessage } = useChatStore()
  const { token } = useAuthStore()

  const sendMessage = async (message: string) => {
    setIsLoading(true)
    
    // Adicionar mensagem do usuário
    addMessage({
      type: 'user',
      content: message
    })

    try {
      // Simular resposta da IA (em produção, fazer chamada real para API)
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const mockResponse: ChatResponse = {
        response: `Entendi! Você quer: "${message}". Vou criar um plano de execução para isso.`,
        plan: {
          steps: [
            {
              name: 'Validar configuração',
              description: 'Verificar parâmetros e pré-requisitos',
              tool: 'validation',
              estimated_time: 5
            },
            {
              name: 'Provisionar recursos',
              description: 'Criar recursos necessários na infraestrutura',
              tool: 'terraform',
              estimated_time: 15
            },
            {
              name: 'Configurar serviços',
              description: 'Aplicar configurações e instalar dependências',
              tool: 'ansible',
              estimated_time: 10
            },
            {
              name: 'Verificar saúde',
              description: 'Executar testes de conectividade e funcionamento',
              tool: 'monitoring',
              estimated_time: 5
            }
          ],
          estimated_duration: 35,
          rollback_plan: [
            {
              name: 'Reverter mudanças',
              description: 'Desfazer alterações em caso de falha',
              tool: 'terraform'
            }
          ],
          validation_checks: [
            'Verificar conectividade de rede',
            'Validar configurações de segurança',
            'Confirmar funcionamento dos serviços'
          ]
        },
        requires_approval: true,
        estimated_duration: 35,
        risk_level: 'medium'
      }

      // Adicionar resposta da IA
      addMessage({
        type: 'ai',
        content: mockResponse.response,
        plan: mockResponse.plan,
        requires_approval: mockResponse.requires_approval,
        estimated_duration: mockResponse.estimated_duration,
        risk_level: mockResponse.risk_level as any
      })

      toast.success('Plano gerado com sucesso!')
      
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      
      addMessage({
        type: 'system',
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.'
      })
      
      toast.error('Erro ao processar mensagem')
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading
  }
}
