# Dialogflow Automation Module

Este módulo fornece uma interface para automatizar a criação e gerenciamento de recursos no Google Dialogflow ES, permitindo a sincronização de intenções e entidades a partir do código ou banco de dados.

## Funcionalidades

- **Gerenciamento de Intenções**: Criação idempotente de intenções com frases de treinamento e respostas.
- **Gerenciamento de Entidades**: (Futuro) Criação e atualização de tipos de entidade.
- **Integração Django**: Comando de gerenciamento para sincronização via CLI.

## Pré-requisitos

1.  **Conta de Serviço do Google Cloud**:
    -   Crie uma conta de serviço no Console do GCP com permissões de `Dialogflow API Admin`.
    -   Baixe o arquivo JSON da chave.

2.  **Variáveis de Ambiente**:
    Configure as seguintes variáveis no seu arquivo `.env`:

    ```env
    DIALOGFLOW_PROJECT_ID=seu-projeto-id
    GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/sua-chave.json
    ```

## Instalação

As dependências já estão incluídas no `requirements.txt` do backend.

```bash
pip install -r backend_admin/requirements.txt
```

## Uso

### Via Código Python

```python
from dialogflow_automation.core.client import DialogflowClient

# Inicializa o cliente
client = DialogflowClient(project_id="meu-projeto", service_account_path="/path/to/creds.json")

# Cria uma intenção (se já existir, retorna a existente)
intent = client.create_intent(
    display_name="Minha Intenção",
    training_phrases_parts=["Olá", "Oi"],
    message_texts=["Olá! Como posso ajudar?"]
)
```

### Via Comando Django (Backend Admin)

O projeto `nexus_admin` inclui um comando de gerenciamento para testar e sincronizar intenções.

```bash
cd backend_admin
python manage.py sync_dialogflow
```

## Testes

Para rodar os testes unitários deste módulo:

```bash
# Na raiz do projeto
export PYTHONPATH=$PYTHONPATH:.
python3 dialogflow_automation/tests/test_client.py
```

Ou via Django test runner (para testes de integração):

```bash
cd backend_admin
python manage.py test core.tests.test_commands
```

## Estrutura

-   `core/client.py`: Lógica principal do cliente Dialogflow.
-   `tests/`: Testes unitários com mocks.
