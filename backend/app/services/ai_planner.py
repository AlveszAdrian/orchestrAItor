"""
Serviço de planejamento com IA
"""

import openai
from typing import Dict, Any, Optional
import structlog
import json

from app.core.config import settings

logger = structlog.get_logger()

class AIPlanner:
    """Serviço de planejamento com IA"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
    async def interpret_command(self, command: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Interpretar comando em linguagem natural
        """
        try:
            logger.info("Interpretando comando", command=command[:100])
            
            # Prompt para interpretação
            system_prompt = """
            Você é um especialista em infraestrutura que interpreta comandos em linguagem natural.
            
            Sua tarefa é:
            1. Entender o que o usuário quer fazer
            2. Identificar os recursos necessários
            3. Determinar o nível de risco
            4. Sugerir uma abordagem
            
            Responda sempre em JSON com:
            {
                "action": "tipo_de_acao",
                "resources": ["lista", "de", "recursos"],
                "risk_level": "low|medium|high|critical",
                "response": "explicação_amigável",
                "requires_approval": true/false
            }
            """
            
            if settings.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": command}
                    ],
                    temperature=0.3
                )
                
                content = response.choices[0].message.content
                return json.loads(content)
            else:
                # Fallback sem IA
                return {
                    "action": "provision",
                    "resources": ["server"],
                    "risk_level": "medium",
                    "response": f"Comando interpretado: {command}",
                    "requires_approval": True
                }
                
        except Exception as e:
            logger.error("Erro na interpretação", error=str(e))
            return {
                "action": "unknown",
                "resources": [],
                "risk_level": "high",
                "response": "Erro ao interpretar comando. Tente ser mais específico.",
                "requires_approval": True
            }
    
    async def generate_plan(self, interpretation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar plano de execução detalhado
        """
        try:
            logger.info("Gerando plano de execução", action=interpretation.get("action"))
            
            action = interpretation.get("action", "unknown")
            resources = interpretation.get("resources", [])
            
            # Templates básicos de plano
            if action == "provision":
                return await self._generate_provision_plan(resources)
            elif action == "configure":
                return await self._generate_configuration_plan(resources)
            elif action == "monitor":
                return await self._generate_monitoring_plan(resources)
            else:
                return {
                    "steps": [
                        {
                            "name": "Análise manual necessária",
                            "description": "Este comando requer análise manual",
                            "tool": "manual",
                            "estimated_time": 30
                        }
                    ],
                    "estimated_duration": 30,
                    "rollback_plan": [],
                    "validation_checks": []
                }
                
        except Exception as e:
            logger.error("Erro na geração do plano", error=str(e))
            raise
    
    async def _generate_provision_plan(self, resources: list) -> Dict[str, Any]:
        """Gerar plano de provisionamento"""
        steps = []
        
        for resource in resources:
            if resource == "server":
                steps.extend([
                    {
                        "name": "Validar configuração",
                        "description": "Verificar parâmetros de configuração",
                        "tool": "validation",
                        "estimated_time": 5
                    },
                    {
                        "name": "Provisionar servidor",
                        "description": "Criar instância do servidor",
                        "tool": "terraform",
                        "estimated_time": 10
                    },
                    {
                        "name": "Configurar servidor",
                        "description": "Aplicar configurações básicas",
                        "tool": "ansible",
                        "estimated_time": 15
                    },
                    {
                        "name": "Verificar saúde",
                        "description": "Executar health checks",
                        "tool": "monitoring",
                        "estimated_time": 5
                    }
                ])
        
        return {
            "steps": steps,
            "estimated_duration": sum(step["estimated_time"] for step in steps),
            "rollback_plan": [
                {
                    "name": "Destruir recursos",
                    "description": "Remover recursos criados",
                    "tool": "terraform"
                }
            ],
            "validation_checks": [
                "Verificar conectividade",
                "Validar configuração",
                "Confirmar serviços ativos"
            ]
        }
    
    async def _generate_configuration_plan(self, resources: list) -> Dict[str, Any]:
        """Gerar plano de configuração"""
        return {
            "steps": [
                {
                    "name": "Backup configuração atual",
                    "description": "Fazer backup antes das mudanças",
                    "tool": "ansible",
                    "estimated_time": 5
                },
                {
                    "name": "Aplicar nova configuração",
                    "description": "Atualizar configurações",
                    "tool": "ansible",
                    "estimated_time": 10
                },
                {
                    "name": "Reiniciar serviços",
                    "description": "Reiniciar serviços afetados",
                    "tool": "ansible",
                    "estimated_time": 5
                }
            ],
            "estimated_duration": 20,
            "rollback_plan": [
                {
                    "name": "Restaurar backup",
                    "description": "Voltar configuração anterior",
                    "tool": "ansible"
                }
            ],
            "validation_checks": [
                "Verificar sintaxe da configuração",
                "Testar conectividade",
                "Validar funcionamento dos serviços"
            ]
        }
    
    async def _generate_monitoring_plan(self, resources: list) -> Dict[str, Any]:
        """Gerar plano de monitoramento"""
        return {
            "steps": [
                {
                    "name": "Instalar agentes",
                    "description": "Instalar agentes de monitoramento",
                    "tool": "ansible",
                    "estimated_time": 10
                },
                {
                    "name": "Configurar dashboards",
                    "description": "Criar dashboards no Grafana",
                    "tool": "grafana",
                    "estimated_time": 15
                },
                {
                    "name": "Configurar alertas",
                    "description": "Definir regras de alerta",
                    "tool": "prometheus",
                    "estimated_time": 10
                }
            ],
            "estimated_duration": 35,
            "rollback_plan": [
                {
                    "name": "Remover monitoramento",
                    "description": "Desinstalar agentes e dashboards",
                    "tool": "ansible"
                }
            ],
            "validation_checks": [
                "Verificar coleta de métricas",
                "Testar alertas",
                "Validar dashboards"
            ]
        }
