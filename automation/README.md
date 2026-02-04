# Automação e Importação de Agentes Dialogflow

Este diretório contém as ferramentas necessárias para automatizar a criação, validação e importação do agente Dialogflow ES para o projeto Nexus AI.

## 📋 Pré-requisitos

### Hardware e Sistema Operacional
- **SO:** Linux, macOS ou Windows.
- **Memória:** Mínimo 4GB RAM (recomendado 8GB para rodar Playwright).
- **Rede:** Acesso à internet para download de binários do navegador e acesso ao Console do Dialogflow.

### Software
- **Python:** 3.10 ou superior.
- **Pip:** Gerenciador de pacotes Python.
- **Navegadores:** Chromium (instalado via Playwright).

## 🛠 Configuração do Ambiente

1. **Instalação de Dependências:**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Estrutura de Arquivos:**
   Certifique-se de que a pasta `automation/dialogflow_schema` contém os arquivos JSON do agente (intents, entities, package.json, agent.json).

## 🚀 Execução da Automação

O script `deploy_agent.py` realiza duas funções principais:
1. **Builder:** Compacta o schema JSON em um arquivo `.zip` compatível com a importação do Dialogflow.
2. **Deploy:** Automatiza a navegação até o console do Dialogflow para importação (requer sessão ativa ou intervenção manual para login).

### Passo a Passo

1. **Validação do Schema (Testes):**
   Antes de gerar o pacote, execute os testes unitários para garantir a integridade do JSON:
   ```bash
   python -m unittest automation/tests/test_schema.py
   ```

2. **Execução do Script:**
   ```bash
   python automation/deploy_agent.py
   ```

### Logs e Resultados Esperados

Ao executar o script, você verá a saída no terminal indicando o progresso:

```text
INFO - Criando arquivo ZIP do agente...
INFO - Arquivo ZIP criado em: automation/dialogflow_agent.zip
INFO - Iniciando automação com Playwright...
INFO - Navegando para https://dialogflow.cloud.google.com/...
```

> **Nota sobre Login:** O script detectará se o login do Google é necessário. Em ambientes CI/CD ou sem cookies persistentes, ele pausará ou tirará um screenshot (`login_required.png`) e encerrará a execução com segurança, pois o login automatizado em contas Google é protegido contra bots.

## 📊 Relatório de Validação

### Testes Unitários
- **Status:** ✅ Aprovado
- **Cobertura:** Validação de estrutura JSON, presença de arquivos obrigatórios (agent.json, package.json).

### Geração de Artefato
- **Arquivo:** `automation/dialogflow_agent.zip`
- **Integridade:** Verificada. Pronto para importação manual ou automática.

### Automação UI (Playwright)
- **Navegação:** ✅ Sucesso ao acessar URL alvo.
- **Detecção de Login:** ✅ Implementada. O script identifica corretamente a barreira de autenticação e salva evidência (`timeout_screenshot.png` ou `login_required.png`).

## ⚠️ Manutenção e Troubleshooting

- **Erro "Schema não encontrado":** Verifique se a pasta `automation/dialogflow_schema` existe.
- **Timeout no Playwright:** Aumente o timeout no script `deploy_agent.py` se a conexão estiver lenta.
- **Login Bloqueado:** Para automação completa em produção, recomenda-se usar a API REST do Dialogflow (Service Account) em vez de automação de UI, ou configurar um perfil de navegador persistente com cookies de sessão.
