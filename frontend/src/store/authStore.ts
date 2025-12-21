import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'operator' | 'viewer'
  full_name: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        try {
          // Simular login - em produção, fazer chamada real para API
          const mockUser: User = {
            id: '1',
            username,
            email: `${username}@byteshift.com`,
            role: 'admin',
            full_name: 'Usuário Demo'
          }
          
          const mockToken = 'demo-token-123'
          
          set({
            user: mockUser,
            token: mockToken,
            isAuthenticated: true
          })
        } catch (error) {
          console.error('Erro no login:', error)
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false
        })
      },

      setUser: (user: User) => {
        set({ user })
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
)
