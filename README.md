# Nexus AI - Plataforma de Autoatendimento Inteligente (GCP Edition)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-MVP%20Ready-green.svg)
![Build Status](https://github.com/devjogerio/dialogflow_ai_gcp_chatbot/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Next.js](https://img.shields.io/badge/next.js-14.0-black)
![GCP](https://img.shields.io/badge/cloud-Google%20Cloud-red)

## 📋 Visão Geral

O **Nexus AI** é uma solução avançada de autoatendimento B2B/B2C projetada para operar nativamente no **Google Cloud Platform (GCP)**. Utilizando o poder da **IA Generativa (Gemini 1.5)** combinada com arquitetura **RAG (Retrieval-Augmented Generation)** via Vertex AI Search, o sistema oferece respostas precisas, contextualizadas e baseadas exclusivamente na documentação oficial da sua empresa.

Além de responder dúvidas técnicas, o Nexus AI atua como um agente ativo capaz de **abrir chamados de suporte** e **gerar orçamentos** instantâneos, integrando-se diretamente aos sistemas de gestão via APIs.

---

## 🚀 Funcionalidades Principais

### 1. Chatbot Inteligente (RAG + LLM)

- **Busca Semântica:** Indexação automática de PDFs, manuais e planilhas armazenados no Cloud Storage via Vertex AI Search.
- **Respostas Humanizadas:** Uso do modelo Gemini 1.5 Flash para sintetizar informações técnicas em linguagem natural acessível.
- **Anti-Alucinação:** O bot é instruído a responder apenas com base no contexto fornecido (Grounding), reduzindo riscos de informações falsas.

### 2. Automação de Processos

- **Abertura de Chamados:** Integração via Dialogflow ES para capturar dados estruturados (Nome, Empresa, Problema) e criar tickets automaticamente no backend Django.
- **Triagem Inteligente:** Classificação automática de prioridade baseada na descrição do problema.

### 3. Dashboard Administrativo

- **Gestão de Tickets:** Interface Django Admin para visualização e acompanhamento de chamados.
- **Controle de Acesso:** Sistema de autenticação e permissões para equipe de suporte.

### 4. Interface Moderna

- **Chat UI Responsiva:** Componente React/Next.js com feedback visual de digitação e histórico de mensagens.
- **Integração Fluida:** Comunicação via API REST com o backend serverless.

---

## 🏗 Arquitetura da Solução

O projeto segue uma arquitetura de microsserviços serverless e event-driven:

```mermaid
graph TD
    User[Usuário] -->|HTTPS| Frontend["Next.js App (Cloud Run)"]
    Frontend -->|API Call| Dialogflow[Dialogflow ES]
    Dialogflow -->|Webhook| CloudFunction[Python Cloud Function]

    subgraph "Google Cloud Platform"
        CloudFunction -->|Query| VertexAI["Vertex AI Search (RAG)"]
        CloudFunction -->|Context + Prompt| Gemini[Gemini 1.5 LLM]
        CloudFunction -->|Create Ticket| DjangoAPI["Django Backend (Cloud Run)"]

        VertexAI -->|Index| GCS["Cloud Storage (PDFs)"]
        DjangoAPI -->|Persist| CloudSQL[PostgreSQL]
    end
```

### Componentes:

1.  **Frontend (Next.js):** Interface do usuário hospedada no Cloud Run ou Vercel.
2.  **Orquestrador (Dialogflow ES):** Gerencia o fluxo de conversação e detecção de intenções.
3.  **Backend Serverless (Cloud Functions):** Cérebro da operação. Recebe o webhook, consulta o RAG e chama o LLM.
4.  **Base de Conhecimento (Vertex AI Search):** Motor de busca vetorial gerenciado.
5.  **Backend Admin (Django):** API REST e Painel Administrativo para persistência de dados.

---

## 🛠 Tecnologias Utilizadas

### Backend Core & AI

- **Python 3.10+**: Linguagem principal.
- **Google Cloud Functions**: Computação serverless.
- **Vertex AI SDK**: Integração com Gemini e modelos generativos.
- **Discovery Engine Client**: Cliente para Vertex AI Search.

### Backend Admin

- **Django 5.0**: Framework web robusto.
- **Django REST Framework**: Construção de APIs.
- **PostgreSQL**: Banco de dados relacional (Cloud SQL).
- **Docker**: Containerização da aplicação.

### Frontend

- **Next.js 14**: Framework React para produção.
- **Tailwind CSS**: Estilização utilitária.
- **TypeScript**: Tipagem estática e segurança de código.

---

## 📦 Estrutura do Projeto

A estrutura de diretórios foi organizada para separar claramente as responsabilidades de cada microsserviço:

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia o nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes sobre o nosso código de conduta e o processo para enviar pull requests.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

```bash
nexus_ai_gcp/
├── backend_admin/          # API Django e Painel Administrativo
│   ├── core/               # Apps do Django (Models, Views)
│   ├── nexus_admin/        # Configurações do projeto Django
│   ├── Dockerfile          # Configuração de container para Cloud Run
│   ├── manage.py           # CLI do Django
│   └── requirements.txt    # Dependências do Django
│
├── backend_functions/      # Cloud Functions (Serverless)
│   ├── main.py             # Entrypoint do Webhook Dialogflow
│   ├── vertex_rag.py       # Lógica de RAG e integração Gemini
│   └── requirements.txt    # Dependências da Cloud Function
│
├── frontend_next/          # Aplicação Next.js
│   ├── src/
│   │   ├── components/     # Componentes React (ChatInterface)
│   │   └── pages/          # Páginas da aplicação
│   └── package.json        # Dependências Node.js
│
└── VERSIONING_ROADMAP.md   # Histórico de versões e changelog
```

---

## ⚙️ Pré-requisitos e Instalação

### Pré-requisitos

- Conta no **Google Cloud Platform** com Billing ativado.
- **gcloud CLI** instalado e autenticado.
- **Python 3.10+** e **Node.js 18+** instalados localmente.
- **Docker** (opcional, para rodar o admin localmente).

### Instalação Passo a Passo

#### 1. Configuração do GCP

Habilite as APIs necessárias:

```bash
gcloud services enable \
  dialogflow.googleapis.com \
  aiplatform.googleapis.com \
  discoveryengine.googleapis.com \
  cloudfunctions.googleapis.com \
  run.googleapis.com
```

#### 2. Backend Admin (Django)

```bash
cd nexus_ai_gcp/backend_admin
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (ver seção abaixo)
# Rodar migrações (requer banco configurado ou SQLite local)
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

#### 3. Backend Serverless (Cloud Functions)

```bash
cd nexus_ai_gcp/backend_functions
# Para testar localmente, use o functions-framework
pip install -r requirements.txt
functions-framework --target=dialogflow_webhook --debug
```

#### 4. Frontend (Next.js)

```bash
cd nexus_ai_gcp/frontend_next
# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

---

## 🔐 Variáveis de Ambiente (.env)

Cada módulo requer suas próprias variáveis de ambiente.

### Backend Admin (.env)

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-django
DATABASE_URL=postgres://user:pass@host:5432/db_name
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Backend Functions (Deploy Environment)

```env
GCP_PROJECT_ID=seu-projeto-gcp-id
GCP_LOCATION=us-central1
DATA_STORE_ID=nexus-docs-store
DJANGO_API_URL=https://seu-backend-django.run.app/api/tickets/
```

---

## 📖 Guia de Uso

### Interagindo com o Chatbot

1. Acesse a interface web em `http://localhost:3000`.
2. Digite uma pergunta técnica, ex: _"Como configuro o servidor X?"_.
   - O sistema buscará no índice do Vertex AI e retornará a resposta.
3. Solicite suporte, ex: _"Quero abrir um chamado"_.
   - O bot coletará seus dados e criará um ticket no Django.

### Acessando o Painel Admin

1. Acesse `http://localhost:8000/admin`.
2. Faça login com superusuário (crie com `python manage.py createsuperuser`).
3. Visualize os chamados criados na seção **Core > Chamados**.

---

## 🚀 Deploy

### Deploy do Backend Admin (Cloud Run)

```bash
gcloud run deploy nexus-admin \
  --source ./nexus_ai_gcp/backend_admin \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy da Cloud Function

```bash
gcloud functions deploy dialogflow-webhook \
  --gen2 \
  --runtime=python310 \
  --region=us-central1 \
  --source=./nexus_ai_gcp/backend_functions \
  --entry-point=dialogflow_webhook \
  --trigger-http \
  --allow-unauthenticated
```

---

## 🤝 Contribuição

1. Faça um Fork do projeto.
2. Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`).
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`).
4. Push para a Branch (`git push origin feature/MinhaFeature`).
5. Abra um Pull Request.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato e Suporte

**Time Nexus AI**

- **Email:** dev@nexus-ai.com
- **Docs:** [docs.nexus-ai.com](https://docs.nexus-ai.com)

---

_Desenvolvido com 💙 e IA Generativa._
