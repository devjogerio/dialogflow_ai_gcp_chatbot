# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-02-05

### Added
- **Backend:** Adicionados testes unitários para models (`Ticket`, `Budget`) e views (`TicketViewSet`) em `backend_admin/core/tests.py`.
- **Backend:** Criada estrutura de configuração do Django (`nexus_admin`) contendo `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`.
- **Docs:** Criado Relatório Técnico de Análise de Código em `docs/technical_report.md`.
- **Docs:** Criado template detalhado de Pull Request em `.github/pull_request_template.md`.
- **Automation:** Script de deploy automatizado do Dialogflow via Playwright (`automation/deploy_agent.py`).

### Changed
- **Backend:** Refatoração de `backend_admin/core/models.py` para conformidade com PEP 8 (espaçamento, comprimento de linha).
- **Backend:** Limpeza de imports não utilizados em `backend_admin/core/views.py`.
- **Backend:** Atualizado `requirements.txt` para comentar temporariamente `psycopg2-binary` (compatibilidade dev local).
- **Frontend:** Correção de sintaxe no `frontend_next/package.json` (remoção de comentários e dependências inválidas).
- **Config:** Atualizado `.gitignore` para incluir padrões Python, Node.js, Django e Next.js.
- **Docs:** Correção de erro de sintaxe Mermaid no `README.md`.

### Fixed
- Erro crítico de inicialização do Django devido à falta do pacote de configurações.
- Erro de sintaxe JSON no frontend que impedia instalação de pacotes.
- Violações de estilo de código (PEP 8) em todo o backend.
- Erro de renderização de diagrama no README.

### Removed
- Dependência `dialogflow-cx-react-web-client` inexistente do frontend.
- Arquivos temporários e branches de feature obsoletas.
