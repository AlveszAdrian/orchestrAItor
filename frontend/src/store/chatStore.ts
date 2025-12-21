import { create } from 'zustand'
import { ChatMessage } from '@/types/chat'

interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  clearMessages: () => void
  setLoading: (loading: boolean) => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,

  addMessage: (messageData) => {
    const message: ChatMessage = {
      ...messageData,
      id: Date.now().toString(),
      timestamp: new Date().toISOString()
    }
    
    set((state) => ({
      messages: [...state.messages, message]
    }))
  },

  clearMessages: () => {
    set({ messages: [] })
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading })
  }
}))
