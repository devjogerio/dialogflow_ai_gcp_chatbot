# Contribuindo para o Nexus AI

Obrigado pelo interesse em contribuir para o Nexus AI! Este documento estabelece as diretrizes para garantir um desenvolvimento organizado e de alta qualidade.

## 🚀 Fluxo de Desenvolvimento (Git Flow)

Adotamos o **Git Flow** para gerenciamento de branches. Por favor, siga a estrutura abaixo:

- **`main`**: Código de produção estável. Protegida (Requer PR e Code Review).
- **`develop`**: Branch de integração principal. Todo desenvolvimento novo deve partir daqui.
- **`feature/nome-da-feature`**: Para novas funcionalidades.
- **`bugfix/nome-do-bug`**: Para correções de bugs não críticos.
- **`hotfix/nome-do-hotfix`**: Para correções críticas em produção.
- **`release/vX.X.X`**: Preparação para nova versão.

### Criando uma Branch

```bash
# Para nova feature
git checkout develop
git checkout -b feature/minha-nova-funcionalidade
```

## 📝 Padrão de Commits

Utilizamos o padrão **Conventional Commits**:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Formatação, ponto e vírgula faltando, etc. (sem alteração de código de produção)
- `refactor:` Refatoração de código
- `test:` Adição ou correção de testes
- `chore:` Atualização de tarefas de build, gerenciador de pacotes, etc.

**Exemplo:**
`feat: adiciona integração com Vertex AI Search`

##  Pull Requests (PR)

1. Garanta que sua branch está atualizada com a `develop`.
2. Rode os testes e linters localmente.
3. Abra o PR apontando para `develop` (ou `main` se for hotfix).
4. Preencha o template do PR com detalhes claros.
5. Aguarde o Code Review de pelo menos um aprovador.

## 🛡️ Padrões de Código

- **Python**: PEP 8.
- **Frontend**: ESLint + Prettier padrão do projeto.
- **Segurança**: Nunca comite chaves de API ou segredos. Use `.env`.

## 🐛 Reportando Bugs

Utilize a aba "Issues" e selecione o template de "Bug Report". Forneça passos para reproduzir, comportamento esperado e logs se possível.
