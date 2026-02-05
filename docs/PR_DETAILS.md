# Pull Request: Implementação de Infraestrutura de Segurança e Deploy

## 📝 Descrição Técnica

Este PR implementa uma infraestrutura robusta de segurança e preparação para deploy em produção no Google Cloud Run. As mudanças abrangem Backend (Django), Frontend (Next.js) e DevOps (Docker/Nginx/CI).

### Principais Mudanças

#### 1. Segurança e Autenticação (Backend)
- **CORS Dinâmico**: Substituição do `CORS_ALLOW_ALL_ORIGINS` por uma whitelist dinâmica baseada em variáveis de ambiente (`CORS_ALLOWED_ORIGINS`).
- **Autenticação via Sessão**: Implementação de `SessionAuthentication` com proteção CSRF rigorosa.
- **Novos Endpoints de Auth**:
  - `POST /api/auth/login/`: Autenticação de usuários.
  - `POST /api/auth/logout/`: Encerramento de sessão.
  - `GET /api/auth/csrf/`: Obtenção segura de token CSRF.
  - `GET /api/auth/user/`: Validação de sessão ativa.
- **Testes Automatizados**: Adição de suítes de teste para CORS (`CORSTest`) e Autenticação (`AuthAPITest`), garantindo cobertura de segurança.

#### 2. Frontend (Next.js)
- **Proteção de Rotas**: HOC `withAuth` para proteger páginas administrativas (`/admin/dashboard`).
- **Fluxo de Login**: Página de login responsiva (`/auth/login`) integrada com a API de autenticação.
- **Gestão de Sessão**: Tratamento automático de cookies `sessionid` e `csrftoken` com `credentials: include`.

#### 3. DevOps e Deploy (Cloud Run)
- **Nginx Otimizado**: Configuração de reverse proxy com compressão Gzip, cache headers e encaminhamento correto de headers (`X-Forwarded-Proto`).
- **Dockerfile Multi-stage**: Otimização da imagem do frontend reduzindo tamanho final e separando build/runtime.
- **CI/CD Pipeline**: Workflow do GitHub Actions (`deploy.yml`) para testes automatizados e deploy contínuo no Cloud Run.

## ✅ Checklist de Implementação

- [x] Backend: Configuração de CORS com suporte a credenciais (`CORS_ALLOW_CREDENTIALS=True`).
- [x] Backend: Middleware e Views de Autenticação implementados.
- [x] Backend: Testes unitários passando (13 testes: Auth, CORS, Tickets).
- [x] Frontend: Página de Login criada e funcional.
- [x] Frontend: Dashboard protegido contra acesso não autorizado.
- [x] DevOps: Dockerfile frontend otimizado (Multi-stage).
- [x] DevOps: Pipeline de CI/CD configurado.

## 🧪 Evidências de Testes

### Testes Automatizados (Backend)
```bash
$ python3 manage.py test core
Found 13 test(s).
Creating test database for alias 'default'...
.............
Ran 13 tests in 6.833s
OK
```

### Validação de Build (Frontend)
```bash
$ npm run build
✓ Creating an optimized production build
✓ Compiled successfully
Route (pages)                              Size     First Load JS
┌ ○ /                                      1.73 kB        83.8 kB
├ ○ /admin/dashboard                       3.08 kB        85.2 kB
└ ○ /auth/login                            2.52 kB        84.6 kB
```

## 🔒 Revisão de Segurança

Solicito atenção especial nos seguintes pontos:
1. **Settings.py**: Verifique se a lógica de `CORS_ALLOWED_ORIGINS` atende aos requisitos de segurança do ambiente de produção.
2. **CSRF**: Confirme se o fluxo de obtenção do token CSRF no frontend está adequado para evitar ataques Cross-Site Request Forgery.
3. **Exposição de Dados**: Garanta que nenhuma informação sensível está sendo retornada nos endpoints de erro.

## 🚀 Próximos Passos (Pós-Merge)

1. Configurar variáveis de ambiente no Cloud Run (`SECRET_KEY`, `DB_PASSWORD`, `CORS_ALLOWED_ORIGINS`).
2. Executar migrations no banco de produção.
3. Validar acesso HTTPS e renovação de certificados SSL gerenciados pelo Google.
