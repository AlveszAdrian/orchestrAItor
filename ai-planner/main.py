"""
AI Planner Service - Módulo de Planejamento com IA
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import structlog
import os

# Configurar logging
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="AI Planner Service",
    description="Serviço de planejamento com IA para automação de infraestrutura",
    version="1.0.0"
)

class PlanRequest(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = None

class PlanResponse(BaseModel):
    interpretation: Dict[str, Any]
    plan: Dict[str, Any]
    risk_assessment: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "AI Planner Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-planner"}

@app.post("/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest):
    """
    Criar plano de execução baseado em comando natural
    """
    try:
        logger.info("Processando solicitação de plano", command=request.command[:100])
        
        # Simular processamento de IA
        # Em produção, aqui seria feita a chamada para OpenAI/Claude
        
        interpretation = {
            "action": "provision",
            "resources": ["server", "nginx"],
            "environment": "production",
            "confidence": 0.95
        }
        
        plan = {
            "steps": [
                {
                    "id": 1,
                    "name": "Validar pré-requisitos",
                    "description": "Verificar quotas, permissões e recursos disponíveis",
                    "tool": "validation",
                    "estimated_time": 5,
                    "dependencies": []
                },
                {
                    "id": 2,
                    "name": "Provisionar infraestrutura",
                    "description": "Criar recursos de infraestrutura usando Terraform",
                    "tool": "terraform",
                    "estimated_time": 15,
                    "dependencies": [1]
                },
                {
                    "id": 3,
                    "name": "Configurar serviços",
                    "description": "Instalar e configurar nginx usando Ansible",
                    "tool": "ansible",
                    "estimated_time": 10,
                    "dependencies": [2]
                },
                {
                    "id": 4,
                    "name": "Verificar saúde",
                    "description": "Executar health checks e testes de conectividade",
                    "tool": "monitoring",
                    "estimated_time": 5,
                    "dependencies": [3]
                }
            ],
            "estimated_duration": 35,
            "rollback_plan": [
                {
                    "name": "Destruir recursos",
                    "description": "Remover todos os recursos criados",
                    "tool": "terraform"
                }
            ],
            "validation_checks": [
                "Verificar conectividade de rede",
                "Validar configurações de segurança",
                "Confirmar funcionamento do nginx"
            ]
        }
        
        risk_assessment = {
            "level": "medium",
            "factors": [
                "Criação de novos recursos",
                "Modificação de configurações de rede",
                "Instalação de software"
            ],
            "mitigation": [
                "Backup automático antes das mudanças",
                "Rollback automático em caso de falha",
                "Monitoramento contínuo durante execução"
            ],
            "requires_approval": True
        }
        
        logger.info("Plano criado com sucesso", 
                   steps_count=len(plan["steps"]),
                   estimated_duration=plan["estimated_duration"],
                   risk_level=risk_assessment["level"])
        
        return PlanResponse(
            interpretation=interpretation,
            plan=plan,
            risk_assessment=risk_assessment
        )
        
    except Exception as e:
        logger.error("Erro ao criar plano", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao criar plano: {str(e)}")

@app.get("/metrics")
async def metrics():
    """Endpoint para métricas do Prometheus"""
    return {
        "plans_created_total": 42,
        "average_plan_duration": 28.5,
        "ai_confidence_avg": 0.87
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
