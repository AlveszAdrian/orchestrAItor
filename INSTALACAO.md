# 🚀 ByteShift Orchestrator - Guia de Instalação

## Visão Geral

O ByteShift Orchestrator é um agente autônomo de IA para automação segura de infraestrutura. Este guia irá te ajudar a instalar e configurar o sistema completo.

## Pré-requisitos

### Software Necessário

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)
- **Git**
- **Make** (opcional, mas recomendado)

### Recursos de Sistema

- **CPU**: 4 cores (mínimo 2)
- **RAM**: 8GB (mínimo 4GB)
- **Disco**: 20GB de espaço livre
- **Rede**: Acesso à internet para downloads

## Instalação Rápida

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd orchestrator
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar configurações (obrigatório!)
nano .env
```

**Configurações importantes no .env:**

```bash
# API Keys (obrigatório para IA funcionar)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Segurança (alterar em produção!)
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ENCRYPTION_KEY=your-32-character-encryption-key

# Database (padrão funciona para desenvolvimento)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/orchestrator
REDIS_URL=redis://redis:6379

# Ambiente
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### 3. Iniciar o Sistema

```bash
# Usando Make (recomendado)
make up

# Ou usando Docker Compose diretamente
docker-compose up -d
```

### 4. Verificar Instalação

```bash
# Verificar status dos serviços
make status

# Ou manualmente
curl http://localhost:8000/health
curl http://localhost:3000
```

## Acessar o Sistema

Após a instalação, você pode acessar:

- **Interface Web**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

### Login Inicial

- **Usuário**: admin
- **Senha**: admin123

⚠️ **Importante**: Altere a senha padrão após o primeiro login!

## Configuração Avançada

### Configurar Provedores de Nuvem

#### AWS
```bash
# No arquivo .env
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1
```

#### Azure
```bash
# No arquivo .env
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
AZURE_TENANT_ID=your-azure-tenant-id
```

#### GCP
```bash
# No arquivo .env
GCP_PROJECT_ID=your-gcp-project-id
GCP_SERVICE_ACCOUNT_KEY=path/to/service-account.json
```

### Configurar Notificações

#### Slack
```bash
# No arquivo .env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

#### Microsoft Teams
```bash
# No arquivo .env
TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR-WEBHOOK
```

## Comandos Úteis

### Desenvolvimento

```bash
# Ver logs em tempo real
make logs

# Ver logs de um serviço específico
make logs-backend
make logs-frontend
make logs-ai

# Reiniciar sistema
make restart

# Parar sistema
make down
```

### Manutenção

```bash
# Backup do banco de dados
make backup

# Restaurar backup
make restore BACKUP_FILE=backup_20240101_120000.sql

# Limpar dados (cuidado!)
make clean

# Atualizar dependências
make update
```

### Monitoramento

```bash
# Verificar status dos serviços
make status

# Ver métricas
make metrics

# Acessar shell do banco
make shell-db

# Acessar shell do backend
make shell-backend
```

## Solução de Problemas

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps postgres

# Reiniciar banco
docker-compose restart postgres

# Ver logs do banco
docker-compose logs postgres
```

#### 2. Frontend não Carrega
```bash
# Verificar logs do frontend
make logs-frontend

# Reconstruir frontend
docker-compose build frontend
docker-compose up -d frontend
```

#### 3. IA não Responde
```bash
# Verificar se OPENAI_API_KEY está configurada
grep OPENAI_API_KEY .env

# Ver logs do AI Planner
make logs-ai

# Testar API diretamente
curl http://localhost:8001/health
```

#### 4. Problemas de Permissão
```bash
# Corrigir permissões (Linux/Mac)
sudo chown -R $USER:$USER .

# Reconstruir containers
make clean
make build
make up
```

### Logs e Debugging

```bash
# Ver todos os logs
make logs

# Ver logs com filtro
docker-compose logs --tail=100 backend

# Modo debug (mais verboso)
# Editar .env: DEBUG=true, LOG_LEVEL=DEBUG
make restart
```

## Configuração de Produção

### 1. Variáveis de Ambiente

```bash
# Criar .env para produção
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Usar senhas fortes
JWT_SECRET_KEY=<senha-super-segura-64-caracteres>
ENCRYPTION_KEY=<chave-32-caracteres-aleatoria>

# Configurar banco externo
DATABASE_URL=postgresql://user:pass@prod-db:5432/orchestrator

# Configurar Redis externo
REDIS_URL=redis://prod-redis:6379
```

### 2. SSL/HTTPS

```bash
# Configurar certificados SSL
# Editar docker-compose.yml para incluir certificados
# Ou usar proxy reverso (nginx, traefik)
```

### 3. Backup Automático

```bash
# Configurar cron para backup diário
0 2 * * * cd /path/to/orchestrator && make backup
```

### 4. Monitoramento

```bash
# Configurar alertas no Grafana
# Configurar notificações para Slack/Teams
# Monitorar métricas de sistema
```

## Desenvolvimento Local

### Executar Serviços Individualmente

```bash
# Backend
make dev-backend

# Frontend
make dev-frontend

# AI Planner
make dev-ai

# Governance
make dev-governance

# Executor
make dev-executor
```

### Testes

```bash
# Executar todos os testes
make test

# Testes específicos
make test-backend
make test-frontend
```

### Linting e Formatação

```bash
# Verificar código
make lint

# Formatar código
make format
```

## Suporte

### Documentação

- **API Docs**: http://localhost:8000/docs
- **README**: Documentação principal do projeto
- **Código**: Comentários inline no código

### Logs Importantes

- **Backend**: `/app/logs/` (dentro do container)
- **Nginx**: `/var/log/nginx/` (se usando nginx)
- **Sistema**: `docker-compose logs`

### Contato

Para suporte técnico ou dúvidas:

1. Verificar logs do sistema
2. Consultar documentação da API
3. Verificar issues conhecidos no repositório
4. Criar issue detalhado se necessário

---

## Próximos Passos

Após a instalação:

1. **Configurar Provedores**: AWS, Azure ou GCP
2. **Criar Usuários**: Adicionar usuários e permissões
3. **Configurar Políticas**: Personalizar governança
4. **Testar Automação**: Executar primeiro comando
5. **Configurar Monitoramento**: Alertas e dashboards

**Parabéns! 🎉 Seu ByteShift Orchestrator está pronto para uso!**
