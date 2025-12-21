export interface ChatMessage {
  id: string
  type: 'user' | 'ai' | 'system'
  content: string
  timestamp: string
  plan?: ExecutionPlan
  requires_approval?: boolean
  estimated_duration?: number
  risk_level?: 'low' | 'medium' | 'high' | 'critical'
}

export interface ExecutionPlan {
  steps: ExecutionStep[]
  estimated_duration: number
  rollback_plan: RollbackStep[]
  validation_checks: string[]
}

export interface ExecutionStep {
  name: string
  description: string
  tool: string
  estimated_time: number
}

export interface RollbackStep {
  name: string
  description: string
  tool: string
}

export interface ChatResponse {
  response: string
  plan?: ExecutionPlan
  requires_approval: boolean
  estimated_duration?: number
  risk_level: string
}
