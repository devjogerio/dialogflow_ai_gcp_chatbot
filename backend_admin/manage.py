#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Adiciona o diretório pai ao sys.path para permitir importação de módulos irmãos (ex: dialogflow_automation)
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Define o módulo de configurações padrão para o projeto 'nexus_admin'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_admin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Executa o comando passado via linha de comando (ex: runserver, migrate)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
