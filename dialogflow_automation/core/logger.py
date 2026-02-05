import logging
import sys

# Configuração de Logger Personalizado
# Define o formato e o nível de logging para a ferramenta de automação.
# Garante que as operações sejam rastreáveis e que erros sejam visíveis no console.

def setup_logger(name="dialogflow_automation"):
    """
    Configura e retorna uma instância de logger.
    
    Args:
        name (str): Nome do logger (padrão: "dialogflow_automation").
    
    Returns:
        logging.Logger: Instância configurada do logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicação de handlers se a função for chamada múltiplas vezes
    if not logger.handlers:
        # Handler para saída no Console (stdout)
        handler = logging.StreamHandler(sys.stdout)
        
        # Formato: Data/Hora - Nome do Logger - Nível - Mensagem
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
