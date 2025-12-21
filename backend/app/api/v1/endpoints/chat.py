"""
Endpoint de chat com IA
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import structlog

from app.core.security import get_current_user
from app.services.ai_planner import AIPlanner
from app.services.governance import GovernanceService

logger = structlog.get_logger()
router = APIRouter()

class ChatMessage(BaseModel):
    """Mensagem de chat"""
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    """Resposta do chat"""
    response: str
    plan: Optional[dict] = None
    requires_approval: bool = False
    estimated_duration: Optional[int] = None
    risk_level: str = "low"

class ChatHistory(BaseModel):
    """Histórico de chat"""
    messages: List[dict]

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """
    Enviar mensagem para o agente de IA
    
    O agente irá:
    1. Interpretar o comando em linguagem natural
    2. Gerar um plano de execução
    3. Validar políticas de governança
    4. Retornar resposta com plano e requisitos
    """
    try:
        logger.info("Processando mensagem do chat", 
                   user_id=current_user["id"], 
                   message=message.message[:100])
        
        # Inicializar serviços
        ai_planner = AIPlanner()
        governance = GovernanceService()
        
        # Interpretar comando
        interpretation = await ai_planner.interpret_command(
            message.message, 
            context=message.context
        )
        
        # Gerar plano
        plan = await ai_planner.generate_plan(interpretation)
        
        # Validar governança
        validation = await governance.validate_plan(plan, current_user)
        
        # Montar resposta
        response = ChatResponse(
            response=interpretation.get("response", "Comando interpretado com sucesso"),
            plan=plan,
            requires_approval=validation.get("requires_approval", True),
            estimated_duration=plan.get("estimated_duration"),
            risk_level=validation.get("risk_level", "medium")
        )
        
        logger.info("Mensagem processada com sucesso", 
                   user_id=current_user["id"],
                   requires_approval=response.requires_approval)
        
        return response
        
    except Exception as e:
        logger.error("Erro ao processar mensagem", 
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )

@router.get("/history", response_model=ChatHistory)
async def get_chat_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Obter histórico de chat do usuário"""
    try:
        # Aqui você buscaria o histórico do banco de dados
        # Por enquanto, retornamos um exemplo
        messages = [
            {
                "id": 1,
                "message": "Provisione um servidor web",
                "response": "Plano criado para provisionar servidor web",
                "timestamp": "2024-01-01T10:00:00Z",
                "type": "user"
            }
        ]
        
        return ChatHistory(messages=messages)
        
    except Exception as e:
        logger.error("Erro ao buscar histórico", 
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico"
        )

@router.delete("/history")
async def clear_chat_history(
    current_user: dict = Depends(get_current_user)
):
    """Limpar histórico de chat do usuário"""
    try:
        # Implementar limpeza do histórico
        logger.info("Histórico de chat limpo", user_id=current_user["id"])
        return {"message": "Histórico limpo com sucesso"}
        
    except Exception as e:
        logger.error("Erro ao limpar histórico", 
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao limpar histórico"
        )
