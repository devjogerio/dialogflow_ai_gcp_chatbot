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
