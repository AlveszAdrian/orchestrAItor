"""
Governance Service - Sistema de Governança e Políticas
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import structlog
import yaml
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
    title="Governance Service",
    description="Sistema de governança e validação de políticas",
    version="1.0.0"
)

class ValidationRequest(BaseModel):
    plan: Dict[str, Any]
    user: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class ValidationResponse(BaseModel):
    valid: bool
    violations: List[str]
    warnings: List[str]
    risk_level: str
    requires_approval: bool
    compliance_score: int

class PolicyEngine:
    """Engine de políticas usando regras YAML"""
    
    def __init__(self):
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """Carregar políticas do arquivo YAML"""
        policies_path = "/app/policies/policies.yaml"
        
        if os.path.exists(policies_path):
            with open(policies_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Políticas padrão se arquivo não existir
        return {
            "resource_limits": {
                "max_servers_per_request": 5,
                "max_cpu_cores": 32,
                "max_memory_gb": 128,
                "allowed_regions": ["us-east-1", "us-west-2", "eu-west-1"]
            },
            "security_policies": {
                "require_encryption": True,
                "require_backup": True,
                "require_monitoring": True,
                "forbidden_ports": [22, 3389, 5432, 3306]
            },
            "approval_policies": {
                "critical_actions": ["delete", "destroy", "terminate"],
                "high_cost_threshold": 1000,
                "production_environments": ["prod", "production"]
            },
            "compliance": {
                "data_residency": True,
                "audit_logging": True,
                "access_control": True
            }
        }
    
    def validate_plan(self, plan: Dict[str, Any], user: Dict[str, Any]) -> ValidationResponse:
        """Validar plano contra políticas"""
        violations = []
        warnings = []
        
        # Validar limites de recursos
        violations.extend(self._validate_resource_limits(plan))
        
        # Validar políticas de segurança
        violations.extend(self._validate_security_policies(plan))
        
        # Validar necessidade de aprovação
        requires_approval = self._check_approval_requirements(plan, user)
        
        # Determinar nível de risco
        risk_level = self._assess_risk_level(plan, violations, warnings)
        
        # Calcular score de compliance
        compliance_score = self._calculate_compliance_score(violations, warnings)
        
        return ValidationResponse(
            valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            risk_level=risk_level,
            requires_approval=requires_approval,
            compliance_score=compliance_score
        )
    
    def _validate_resource_limits(self, plan: Dict[str, Any]) -> List[str]:
        """Validar limites de recursos"""
        violations = []
        steps = plan.get("steps", [])
        
        # Contar recursos a serem provisionados
        server_count = sum(1 for step in steps if "servidor" in step.get("description", "").lower())
        
        if server_count > self.policies["resource_limits"]["max_servers_per_request"]:
            violations.append(
                f"Excede limite de servidores: {server_count} > "
                f"{self.policies['resource_limits']['max_servers_per_request']}"
            )
        
        return violations
    
    def _validate_security_policies(self, plan: Dict[str, Any]) -> List[str]:
        """Validar políticas de segurança"""
        violations = []
        
        # Verificar se requer criptografia
        if self.policies["security_policies"]["require_encryption"]:
            # Implementar verificação específica
            pass
        
        return violations
    
    def _check_approval_requirements(self, plan: Dict[str, Any], user: Dict[str, Any]) -> bool:
        """Verificar se requer aprovação"""
        user_role = user.get("role", "viewer")
        
        # Usuários viewer sempre requerem aprovação
        if user_role == "viewer":
            return True
        
        # Ações críticas requerem aprovação
        steps = plan.get("steps", [])
        for step in steps:
            description = step.get("description", "").lower()
            for critical_action in self.policies["approval_policies"]["critical_actions"]:
                if critical_action in description:
                    return True
        
        # Duração longa requer aprovação
        if plan.get("estimated_duration", 0) > 60:
            return True
        
        return False
    
    def _assess_risk_level(self, plan: Dict[str, Any], violations: List[str], warnings: List[str]) -> str:
        """Avaliar nível de risco"""
        if violations:
            return "high"
        elif warnings:
            return "medium"
        elif plan.get("estimated_duration", 0) > 30:
            return "medium"
        else:
            return "low"
    
    def _calculate_compliance_score(self, violations: List[str], warnings: List[str]) -> int:
        """Calcular score de compliance"""
        base_score = 100
        base_score -= len(violations) * 20
        base_score -= len(warnings) * 5
        return max(0, base_score)

# Instância global do engine de políticas
policy_engine = PolicyEngine()

@app.get("/")
async def root():
    return {"message": "Governance Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "governance"}

@app.post("/validate", response_model=ValidationResponse)
async def validate_plan(request: ValidationRequest):
    """
    Validar plano contra políticas de governança
    """
    try:
        logger.info("Validando plano", user_id=request.user.get("id"))
        
        result = policy_engine.validate_plan(request.plan, request.user)
        
        logger.info("Validação concluída", 
                   valid=result.valid,
                   violations_count=len(result.violations),
                   risk_level=result.risk_level,
                   compliance_score=result.compliance_score)
        
        return result
        
    except Exception as e:
        logger.error("Erro na validação", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro na validação: {str(e)}")

@app.get("/policies")
async def get_policies():
    """Obter políticas ativas"""
    return {
        "policies": policy_engine.policies,
        "total_policies": len(policy_engine.policies),
        "last_updated": "2024-01-01T00:00:00Z"
    }

@app.get("/metrics")
async def metrics():
    """Endpoint para métricas do Prometheus"""
    return {
        "validations_total": 156,
        "violations_total": 12,
        "average_compliance_score": 87.5
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
