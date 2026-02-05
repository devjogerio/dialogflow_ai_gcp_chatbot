import os
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import AlreadyExists, GoogleAPICallError, NotFound
from .logger import setup_logger

# Inicializa o logger para o cliente Dialogflow
logger = setup_logger("dialogflow_client")


class DialogflowClient:
    """
    Wrapper para a API do Google Cloud Dialogflow ES.
    Facilita a criação programática de Agentes, Intenções, Entidades e Contextos.
    Encapsula a complexidade da API do Google Cloud, fornecendo métodos de alto nível.
    """

    def __init__(self, project_id, service_account_path):
        """
        Inicializa o cliente com as credenciais do Google Cloud.

        Args:
            project_id (str): ID do projeto no Google Cloud (ex: nexus-ai-aws-v1-ahuj).
            service_account_path (str): Caminho absoluto ou relativo para o arquivo JSON da Service Account.

        Exceções:
            Pode lançar erros de autenticação se as credenciais forem inválidas.
        """
        self.project_id = project_id

        # Define a variável de ambiente necessária para a biblioteca google-cloud-dialogflow autenticar
        # Isso é uma prática comum para autenticação baseada em arquivo local
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

        # Inicializa os clientes específicos da API
        self.intents_client = dialogflow.IntentsClient()
        self.entity_types_client = dialogflow.EntityTypesClient()
        self.agents_client = dialogflow.AgentsClient()

        # Define o caminho "pai" (parent) padrão para o agente no projeto
        # Formato: projects/<Project ID>/agent
        self.parent = f"projects/{project_id}/agent"

        logger.info(
            f"Cliente Dialogflow inicializado para o projeto: {project_id}")

    def create_intent(self, display_name, training_phrases_parts, message_texts, parameters=None, input_context_names=None, output_contexts=None):
        """
        Cria uma nova intenção (Intent) no Dialogflow.
        Implementa idempotência verificando se a intenção já existe (pelo nome de exibição).
        Se existir, tenta atualizar (ou ignorar, dependendo da estratégia - aqui optamos por ignorar/logar).

        Args:
            display_name (str): Nome de exibição único da intenção.
            training_phrases_parts (list): Lista de frases de exemplo que o usuário pode dizer.
            message_texts (list): Lista de respostas textuais que o bot enviará.
            parameters (list, optional): Lista de dicionários para extração de entidades (slots).
            input_context_names (list, optional): Lista de nomes de contextos de entrada.
            output_contexts (list, optional): Lista de dicionários definindo contextos de saída.

        Returns:
            google.cloud.dialogflow_v2.types.Intent: Objeto da intenção criada ou existente.
        """
        logger.info(f"Iniciando criação da intenção: {display_name}")

        try:
            # Verifica se a intenção já existe para garantir idempotência
            existing_intent = self._get_intent_by_display_name(display_name)
            if existing_intent:
                logger.warning(
                    f"A intenção '{display_name}' já existe. Ignorando criação para manter idempotência.")
                return existing_intent

            # 1. Constrói as frases de treinamento (Training Phrases)
            # Cada frase é convertida no formato exigido pela API (Parts)
            training_phrases = []
            for phrase_text in training_phrases_parts:
                part = dialogflow.Intent.TrainingPhrase.Part(text=phrase_text)
                training_phrase = dialogflow.Intent.TrainingPhrase(parts=[
                                                                   part])
                training_phrases.append(training_phrase)

            # 2. Constrói a mensagem de resposta (Response Message)
            # Suporta múltiplas variações de texto para a mesma resposta
            text = dialogflow.Intent.Message.Text(text=message_texts)
            message = dialogflow.Intent.Message(text=text)

            # 3. Constrói os parâmetros (Entidades a serem extraídas)
            intent_parameters = []
            if parameters:
                for param in parameters:
                    new_param = dialogflow.Intent.Parameter(
                        display_name=param['display_name'],
                        entity_type_display_name=param['entity_type_display_name'],
                        mandatory=param.get('mandatory', False),
                        prompts=param.get('prompts', [])
                    )
                    intent_parameters.append(new_param)

            # 4. Configura Contextos de Saída (Output Contexts)
            output_contexts_objects = []
            if output_contexts:
                for ctx in output_contexts:
                    # O nome do contexto deve ser o caminho completo
                    ctx_name = f"{self.parent}/sessions/-/contexts/{ctx['name']}"
                    context = dialogflow.Context(
                        name=ctx_name,
                        lifespan_count=ctx.get('lifespan_count', 5)
                    )
                    output_contexts_objects.append(context)

            # 5. Monta o objeto Intent completo
            intent = dialogflow.Intent(
                display_name=display_name,
                training_phrases=training_phrases,
                messages=[message],
                parameters=intent_parameters,
                input_context_names=[
                    f"{self.parent}/sessions/-/contexts/{name}" for name in input_context_names] if input_context_names else [],
                output_contexts=output_contexts_objects
            )

            # 6. Chama a API para criar a intenção
            response = self.intents_client.create_intent(
                request={"parent": self.parent, "intent": intent}
            )

            logger.info(f"Intenção criada com sucesso: {response.name}")
            return response

        except GoogleAPICallError as e:
            logger.error(
                f"Erro de API ao criar intenção '{display_name}': {e}")
            raise
        except Exception as e:
            logger.error(
                f"Erro inesperado ao criar intenção '{display_name}': {e}")
            raise

    def create_entity_type(self, display_name, kind, entities):
        """
        Cria um novo Tipo de Entidade (Entity Type) customizado.

        Args:
            display_name (str): Nome da entidade (ex: 'TiposDeServico').
            kind (str): Tipo da entidade ('KIND_MAP' para sinônimos ou 'KIND_LIST').
            entities (list): Lista de dicionários com 'value' e 'synonyms'.
        """
        logger.info(f"Criando tipo de entidade: {display_name}")

        try:
            # Verifica existência prévia
            # (Simplificação: tenta criar e captura AlreadyExists se necessário,
            # mas a API do Dialogflow lança erro genérico se nome duplicado)

            # Mapeia string de 'kind' para o enum da API
            kind_map = {
                'KIND_MAP': dialogflow.EntityType.Kind.KIND_MAP,
                'KIND_LIST': dialogflow.EntityType.Kind.KIND_LIST
            }
            entity_kind = kind_map.get(
                kind, dialogflow.EntityType.Kind.KIND_MAP)

            # Cria lista de objetos Entity
            entity_objects = []
            for ent in entities:
                entity_objects.append(dialogflow.EntityType.Entity(
                    value=ent['value'],
                    synonyms=ent['synonyms']
                ))

            entity_type = dialogflow.EntityType(
                display_name=display_name,
                kind=entity_kind,
                entities=entity_objects
            )

            response = self.entity_types_client.create_entity_type(
                parent=self.parent,
                entity_type=entity_type
            )
            logger.info(f"Tipo de entidade criado: {response.name}")
            return response

        except AlreadyExists:
            logger.warning(f"Entidade '{display_name}' já existe. Ignorando.")
        except Exception as e:
            error_msg = str(e)
            # Dialogflow pode retornar 409 (Conflict) ou 400 (FailedPrecondition) se já existe
            if "409" in error_msg or "already exists" in error_msg:
                logger.warning(
                    f"Entidade '{display_name}' já existe (detectado via erro API). Ignorando.")
            else:
                logger.error(f"Erro ao criar entidade '{display_name}': {e}")
                raise

    def _get_intent_by_display_name(self, display_name):
        """
        Método auxiliar privado para buscar uma intenção pelo nome de exibição.
        Necessário pois a API usa UUIDs para identificação, mas nós usamos nomes legíveis.

        Args:
            display_name (str): Nome de exibição a procurar.

        Returns:
            Intent object ou None se não encontrado.
        """
        try:
            # Lista todas as intenções (paginação simplificada para exemplo)
            # Em produção, deve-se iterar pelas páginas
            intents = self.intents_client.list_intents(
                request={"parent": self.parent})

            for intent in intents:
                if intent.display_name == display_name:
                    return intent
            return None
        except Exception as e:
            logger.error(f"Erro ao listar intenções para busca: {e}")
            return None

    def list_intents(self):
        """
        Lista todas as intenções existentes no agente.
        Útil para validação ou limpeza antes do sync.
        """
        return self.intents_client.list_intents(request={"parent": self.parent})
        logger.info("Listando intenções existentes...")
        intents = self.intents_client.list_intents(
            request={"parent": self.parent})
        for intent in intents:
            logger.info(
                f"Encontrada: {intent.display_name} (ID: {intent.name})")
        return intents
