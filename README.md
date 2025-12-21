# Agente Autônomo de Infraestrutura com Governança

## Visão Geral

Sistema de IA que executa tarefas de infraestrutura de forma segura, auditável e governada, permitindo comandos em linguagem natural para provisionamento, configuração, operação e correção automatizada.

## Arquitetura

```
Interface Web → Planner IA → Validador/Governança → Executor → Observabilidade/Self-Healing
```

## Componentes Principais

- **Frontend**: Interface web com Next.js para interação via chat/formulários
- **Backend**: API FastAPI para orquestração e controle
- **AI Planner**: Módulo de IA para interpretação e planejamento
- **Governança**: Sistema de políticas e validação de segurança
- **Executor**: Execução controlada via GitOps
- **Observabilidade**: Monitoramento e self-healing

## Tecnologias

- **Frontend**: Next.js, React, TypeScript
- **Backend**: FastAPI, Python, SQLAlchemy
- **IA**: OpenAI/Claude API, LangChain
- **Infraestrutura**: Terraform, Ansible, Helm
- **Governança**: OPA, Checkov
- **Observabilidade**: Prometheus, Grafana
- **Orquestração**: Docker, Docker Compose

## Estrutura do Projeto

```
orchestrator/
├── frontend/          # Interface web Next.js
├── backend/           # API FastAPI
├── ai-planner/        # Módulo de planejamento IA
├── governance/        # Sistema de governança
├── executor/          # Executor de infraestrutura
├── observability/     # Monitoramento e logs
├── infrastructure/    # Terraform/Ansible templates
└── docker/           # Configurações Docker
```

## Instalação e Execução

### Pré-requisitos

- Docker e Docker Compose
- Node.js 18+
- Python 3.11+
- Terraform
- Ansible

### Execução Local

```bash
# Clonar o repositório
git clone <repo-url>
cd orchestrator

# Executar com Docker Compose
docker-compose up -d

# Ou executar individualmente
cd backend && python -m uvicorn main:app --reload
cd frontend && npm run dev
```

## Roadmap

### Fase 1 - MVP ✅
- [x] Interface básica
- [x] Planner IA simples
- [x] Executor via pipeline
- [x] Tratamento básico de erro

### Fase 2 - Governança Avançada
- [ ] Policies e compliance
- [ ] RBAC completo
- [ ] Observabilidade integrada

### Fase 3 - Autonomia Controlada
- [ ] Self-healing completo
- [ ] Automação complexa multi-servidor
- [ ] Catálogo de operações prontas

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

MIT License
