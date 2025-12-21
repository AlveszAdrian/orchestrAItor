"""
Serviço de governança e políticas
"""

from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()

class GovernanceService:
    """Serviço de governança e validação de políticas"""
    
    def __init__(self):
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """Carregar políticas de governança"""
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
                "high_cost_threshold": 1000,  # USD por mês
                "production_environments": ["prod", "production"]
            },
            "compliance": {
                "data_residency": True,
                "audit_logging": True,
                "access_control": True
            }
        }
    
    async def validate_plan(self, plan: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar plano contra políticas de governança
        """
        try:
            logger.info("Validando plano contra políticas", user_id=user.get("id"))
            
            violations = []
            warnings = []
            risk_level = "low"
            requires_approval = False
            
            # Validar limites de recursos
            resource_violations = self._validate_resource_limits(plan)
            violations.extend(resource_violations)
            
            # Validar políticas de segurança
            security_violations = self._validate_security_policies(plan)
            violations.extend(security_violations)
            
            # Validar necessidade de aprovação
            approval_required = self._check_approval_requirements(plan, user)
            requires_approval = approval_required or len(violations) > 0
            
            # Determinar nível de risco
            if violations:
                risk_level = "high"
            elif warnings:
                risk_level = "medium"
            elif requires_approval:
                risk_level = "medium"
            
            result = {
                "valid": len(violations) == 0,
                "violations": violations,
                "warnings": warnings,
                "risk_level": risk_level,
                "requires_approval": requires_approval,
                "compliance_score": self._calculate_compliance_score(violations, warnings)
            }
            
            logger.info("Validação concluída", 
                       valid=result["valid"],
                       violations_count=len(violations),
                       risk_level=risk_level)
            
            return result
            
        except Exception as e:
            logger.error("Erro na validação de governança", error=str(e))
            return {
                "valid": False,
                "violations": ["Erro interno na validação"],
                "warnings": [],
                "risk_level": "critical",
                "requires_approval": True,
                "compliance_score": 0
            }
    
    def _validate_resource_limits(self, plan: Dict[str, Any]) -> List[str]:
        """Validar limites de recursos"""
        violations = []
        steps = plan.get("steps", [])
        
        # Contar servidores a serem provisionados
        server_count = sum(1 for step in steps if "servidor" in step.get("description", "").lower())
        
        if server_count > self.policies["resource_limits"]["max_servers_per_request"]:
            violations.append(
                f"Excede limite de servidores por requisição: {server_count} > "
                f"{self.policies['resource_limits']['max_servers_per_request']}"
            )
        
        return violations
    
    def _validate_security_policies(self, plan: Dict[str, Any]) -> List[str]:
        """Validar políticas de segurança"""
        violations = []
        
        # Verificar se requer criptografia
        if self.policies["security_policies"]["require_encryption"]:
            # Implementar verificação de criptografia
            pass
        
        # Verificar se requer backup
        if self.policies["security_policies"]["require_backup"]:
            # Implementar verificação de backup
            pass
        
        return violations
    
    def _check_approval_requirements(self, plan: Dict[str, Any], user: Dict[str, Any]) -> bool:
        """Verificar se requer aprovação"""
        
        # Ações críticas sempre requerem aprovação
        steps = plan.get("steps", [])
        for step in steps:
            description = step.get("description", "").lower()
            for critical_action in self.policies["approval_policies"]["critical_actions"]:
                if critical_action in description:
                    return True
        
        # Usuários com role viewer sempre requerem aprovação
        user_role = user.get("role", "viewer")
        if user_role == "viewer":
            return True
        
        # Duração estimada alta requer aprovação
        estimated_duration = plan.get("estimated_duration", 0)
        if estimated_duration > 60:  # mais de 1 hora
            return True
        
        return False
    
    def _calculate_compliance_score(self, violations: List[str], warnings: List[str]) -> int:
        """Calcular score de compliance (0-100)"""
        base_score = 100
        
        # Deduzir pontos por violações
        base_score -= len(violations) * 20
        base_score -= len(warnings) * 5
        
        return max(0, base_score)
    
    async def get_policy_summary(self) -> Dict[str, Any]:
        """Obter resumo das políticas ativas"""
        return {
            "total_policies": len(self.policies),
            "categories": list(self.policies.keys()),
            "last_updated": "2024-01-01T00:00:00Z",
            "compliance_required": True
        }
    
    async def validate_user_permissions(self, user: Dict[str, Any], action: str) -> bool:
        """Validar permissões do usuário para uma ação"""
        user_role = user.get("role", "viewer")
        
        # Mapeamento de permissões por role
        permissions = {
            "admin": ["create", "read", "update", "delete", "execute", "approve"],
            "operator": ["create", "read", "update", "execute"],
            "viewer": ["read"]
        }
        
        allowed_actions = permissions.get(user_role, [])
        return action in allowed_actions
