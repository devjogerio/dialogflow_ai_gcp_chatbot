import json
import os
from .logger import setup_logger

# Inicializa o logger para este módulo
logger = setup_logger("config_parser")


class ConfigParser:
    """
    Classe responsável por ler e validar arquivos de configuração (Intents, Entidades).
    Centraliza o acesso aos dados JSON que definem a estrutura do Chatbot.
    """

    def __init__(self, config_path):
        """
        Inicializa o parser com o caminho para o diretório de configuração.

        Args:
            config_path (str): Caminho relativo ou absoluto para a pasta de configs.
        """
        self.config_path = config_path
        # Valida se o diretório existe imediatamente
        if not os.path.exists(self.config_path):
            logger.error(
                f"Diretório de configuração não encontrado: {self.config_path}")
            raise FileNotFoundError(
                f"Config path not found: {self.config_path}")

    def load_intents(self, filename="intents.json"):
        """
        Carrega e valida a lista de intenções do arquivo JSON.

        Args:
            filename (str): Nome do arquivo JSON contendo as intenções.

        Returns:
            list: Lista de dicionários contendo a definição das intenções.
        """
        file_path = os.path.join(self.config_path, filename)
        logger.info(f"Carregando intenções de: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                intents = json.load(f)

            # Validação básica de esquema
            if not isinstance(intents, list):
                raise ValueError(
                    "O arquivo de intents deve conter uma lista JSON.")

            for index, intent in enumerate(intents):
                self._validate_intent_schema(intent, index)

            logger.info(f"{len(intents)} intenções carregadas com sucesso.")
            return intents

        except FileNotFoundError:
            logger.error(f"Arquivo de intenções não encontrado: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erro de sintaxe no JSON de intenções: {e}")
            raise

    def _validate_intent_schema(self, intent, index):
        """
        Valida se um dicionário de intenção possui os campos obrigatórios e tipos corretos.

        Args:
            intent (dict): Dicionário representando a intenção.
            index (int): Índice da intenção na lista (para logs de erro).

        Raises:
            ValueError: Se o schema for inválido.
        """
        required_fields = {
            "display_name": str,
            "training_phrases": list,
            "messages": list
        }

        # Valida campos obrigatórios de nível superior
        for field, expected_type in required_fields.items():
            if field not in intent:
                raise ValueError(
                    f"Intenção #{index}: Campo obrigatório '{field}' ausente.")
            if not isinstance(intent[field], expected_type):
                raise ValueError(
                    f"Intenção #{index}: Campo '{field}' deve ser do tipo {expected_type.__name__}.")

        # Valida conteúdo das listas
        if not all(isinstance(phrase, str) for phrase in intent["training_phrases"]):
            raise ValueError(
                f"Intenção #{index} ({intent['display_name']}): 'training_phrases' deve conter apenas strings.")

        if not all(isinstance(msg, str) for msg in intent["messages"]):
            raise ValueError(
                f"Intenção #{index} ({intent['display_name']}): 'messages' deve conter apenas strings.")

        # Valida parâmetros opcionais
        if "parameters" in intent:
            if not isinstance(intent["parameters"], list):
                raise ValueError(
                    f"Intenção #{index} ({intent['display_name']}): 'parameters' deve ser uma lista.")

            for param_idx, param in enumerate(intent["parameters"]):
                self._validate_parameter_schema(param, index, param_idx)

    def _validate_parameter_schema(self, param, intent_index, param_index):
        """Valida a estrutura de um parâmetro."""
        required_param_fields = ["display_name",
                                 "entity_type_display_name", "mandatory"]

        for field in required_param_fields:
            if field not in param:
                raise ValueError(
                    f"Intenção #{intent_index}, Parâmetro #{param_index}: Campo '{field}' ausente.")
