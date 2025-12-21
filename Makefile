# Makefile para ByteShift Orchestrator
# Comandos para desenvolvimento e deploy

.PHONY: help build up down logs clean install test lint format

# Variáveis
COMPOSE_FILE = docker-compose.yml
PROJECT_NAME = orchestrator

help: ## Mostrar esta ajuda
	@echo "ByteShift Orchestrator - Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Desenvolvimento
install: ## Instalar dependências
	@echo "Instalando dependências do backend..."
	cd backend && pip install -r requirements.txt
	@echo "Instalando dependências do frontend..."
	cd frontend && npm install
	@echo "Instalando dependências dos serviços..."
	cd ai-planner && pip install -r requirements.txt
	cd governance && pip install -r requirements.txt
	cd executor && pip install -r requirements.txt

build: ## Construir todas as imagens Docker
	@echo "Construindo imagens Docker..."
	docker-compose -f $(COMPOSE_FILE) build

up: ## Iniciar todos os serviços
	@echo "Iniciando ByteShift Orchestrator..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "Serviços iniciados! Acesse:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend API: http://localhost:8000"
	@echo "  Grafana: http://localhost:3001 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"

down: ## Parar todos os serviços
	@echo "Parando serviços..."
	docker-compose -f $(COMPOSE_FILE) down

restart: down up ## Reiniciar todos os serviços

logs: ## Mostrar logs de todos os serviços
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## Mostrar logs do backend
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Mostrar logs do frontend
	docker-compose -f $(COMPOSE_FILE) logs -f frontend

logs-ai: ## Mostrar logs do AI Planner
	docker-compose -f $(COMPOSE_FILE) logs -f ai-planner

logs-governance: ## Mostrar logs do Governance
	docker-compose -f $(COMPOSE_FILE) logs -f governance

logs-executor: ## Mostrar logs do Executor
	docker-compose -f $(COMPOSE_FILE) logs -f executor

# Desenvolvimento local
dev-backend: ## Executar backend em modo desenvolvimento
	cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Executar frontend em modo desenvolvimento
	cd frontend && npm run dev

dev-ai: ## Executar AI Planner em modo desenvolvimento
	cd ai-planner && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

dev-governance: ## Executar Governance em modo desenvolvimento
	cd governance && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002

dev-executor: ## Executar Executor em modo desenvolvimento
	cd executor && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8003

# Testes
test: ## Executar todos os testes
	@echo "Executando testes do backend..."
	cd backend && python -m pytest
	@echo "Executando testes do frontend..."
	cd frontend && npm test
	@echo "Executando testes dos serviços..."
	cd ai-planner && python -m pytest
	cd governance && python -m pytest
	cd executor && python -m pytest

test-backend: ## Executar testes do backend
	cd backend && python -m pytest -v

test-frontend: ## Executar testes do frontend
	cd frontend && npm test

# Linting e formatação
lint: ## Executar linting em todos os projetos
	@echo "Linting backend..."
	cd backend && python -m black . --check
	cd backend && python -m isort . --check-only
	cd backend && python -m mypy .
	@echo "Linting frontend..."
	cd frontend && npm run lint

format: ## Formatar código
	@echo "Formatando backend..."
	cd backend && python -m black .
	cd backend && python -m isort .
	@echo "Formatando frontend..."
	cd frontend && npm run lint --fix

# Database
db-migrate: ## Executar migrações do banco
	cd backend && alembic upgrade head

db-reset: ## Reset do banco de dados
	docker-compose -f $(COMPOSE_FILE) down -v
	docker-compose -f $(COMPOSE_FILE) up -d postgres
	sleep 5
	docker-compose -f $(COMPOSE_FILE) up -d

# Monitoramento
status: ## Verificar status dos serviços
	@echo "Status dos serviços:"
	@curl -s http://localhost:8000/health | jq . || echo "Backend: ❌ Offline"
	@curl -s http://localhost:8001/health | jq . || echo "AI Planner: ❌ Offline"
	@curl -s http://localhost:8002/health | jq . || echo "Governance: ❌ Offline"
	@curl -s http://localhost:8003/health | jq . || echo "Executor: ❌ Offline"

metrics: ## Mostrar métricas dos serviços
	@echo "Métricas dos serviços:"
	@curl -s http://localhost:8000/api/v1/metrics || echo "Backend metrics: N/A"
	@curl -s http://localhost:8001/metrics || echo "AI Planner metrics: N/A"
	@curl -s http://localhost:8002/metrics || echo "Governance metrics: N/A"
	@curl -s http://localhost:8003/metrics || echo "Executor metrics: N/A"

# Limpeza
clean: ## Limpar containers, volumes e imagens
	@echo "Limpando recursos Docker..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f
	docker volume prune -f

clean-all: clean ## Limpeza completa (incluindo imagens)
	docker image prune -a -f

# Backup e restore
backup: ## Fazer backup do banco de dados
	@echo "Fazendo backup do banco de dados..."
	docker-compose -f $(COMPOSE_FILE) exec postgres pg_dump -U postgres orchestrator > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup salvo como backup_$(shell date +%Y%m%d_%H%M%S).sql"

restore: ## Restaurar backup do banco (usar BACKUP_FILE=arquivo.sql)
	@if [ -z "$(BACKUP_FILE)" ]; then echo "Use: make restore BACKUP_FILE=backup.sql"; exit 1; fi
	@echo "Restaurando backup $(BACKUP_FILE)..."
	docker-compose -f $(COMPOSE_FILE) exec -T postgres psql -U postgres orchestrator < $(BACKUP_FILE)

# Deploy
deploy-prod: ## Deploy para produção
	@echo "Deploy para produção..."
	@echo "⚠️  Certifique-se de ter configurado as variáveis de ambiente!"
	docker-compose -f docker-compose.prod.yml up -d --build

# Utilitários
shell-backend: ## Abrir shell no container do backend
	docker-compose -f $(COMPOSE_FILE) exec backend bash

shell-db: ## Abrir shell no banco de dados
	docker-compose -f $(COMPOSE_FILE) exec postgres psql -U postgres orchestrator

update: ## Atualizar dependências
	@echo "Atualizando dependências..."
	cd backend && pip install --upgrade -r requirements.txt
	cd frontend && npm update
	cd ai-planner && pip install --upgrade -r requirements.txt
	cd governance && pip install --upgrade -r requirements.txt
	cd executor && pip install --upgrade -r requirements.txt
