# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Next.js build (produces .next/standalone and .next/static)
RUN npm run build

# Stage 2: Production (Node + Nginx)
FROM nginx:alpine AS production
WORKDIR /app

# Install Node.js (required for Next.js standalone server)
RUN apk add --no-cache nodejs

# Copy Nginx Config
COPY nginx.conf /etc/nginx/http.d/default.conf

# Copy Next.js Build Artifacts
# Standalone folder contains the server and dependencies
COPY --from=builder /app/.next/standalone ./
# Static files are NOT included in standalone, so we copy them
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Copy Startup Script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Cloud Run expects port 8080
EXPOSE 8080

CMD ["/start.sh"]
# Etapa 1: Dependências
FROM node:18-alpine AS deps
WORKDIR /app

# Copia arquivos de dependência
COPY package.json package-lock.json ./ 

# Instala dependências (ci é mais rápido e confiável para builds)
RUN npm ci

# Etapa 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Desabilita telemetria do Next.js
ENV NEXT_TELEMETRY_DISABLED 1

# Build do projeto
RUN npm run build

# Etapa 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Cria usuário não-root por segurança
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copia arquivos necessários do builder
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
# O Next.js standalone server escuta na porta definida em PORT
CMD ["node", "server.js"]
