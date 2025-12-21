FROM node:18-alpine

# Instalar dependências do sistema
RUN apk add --no-cache libc6-compat

# Configurar diretório de trabalho
WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# Criar usuário não-root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Definir permissões
USER nextjs

# Expor porta
EXPOSE 3000

ENV PORT 3000

# Comando de inicialização
CMD ["npm", "start"]
