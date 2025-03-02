# src/utils/environment_loader.py
import os
import sys
from dotenv import load_dotenv
import argparse

def load_environment():
    """
    Carrega variáveis de ambiente e determina o ambiente de execução.
    
    A função primeiro tenta carregar do arquivo .env, depois considera 
    variáveis de ambiente e argumentos de linha de comando.
    
    Returns:
        str: O ambiente carregado ('development' ou 'production')
    """
    # Carrega as variáveis de ambiente do arquivo .env
    # Prioridade: .env (com valores específicos) > variáveis de sistema
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    load_dotenv(dotenv_path, override=True)
    
    # Verifica se o ambiente já está definido nas variáveis carregadas
    env = os.environ.get('ENVIRONMENT', '').lower()
    if env in ['development', 'production']:
        print(f"Environment loaded from .env: {env}")
        return env
    
    # Verifica argumentos da linha de comando
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--env', dest='environment', 
                        choices=['development', 'production'],
                        help='Set environment (development or production)')
    
    # Tenta fazer o parse, mas ignora erros
    try:
        args, _ = parser.parse_known_args()
        if args.environment:
            env = args.environment
            os.environ['ENVIRONMENT'] = env
            print(f"Environment set from command line: {env}")
            return env
    except Exception as e:
        print(f"Warning: {e}")
    
    # Valor padrão se nada for especificado
    default_env = 'development'
    os.environ['ENVIRONMENT'] = default_env
    print(f"Using default environment: {default_env}")
    return default_env

# Carrega o ambiente imediatamente quando o módulo é importado
environment = load_environment()

# Debug: mostre todas as variáveis de ambiente carregadas para diagnóstico
if os.environ.get('DEBUG_MODE', '').lower() in ('true', '1', 'yes'):
    print("\nLoaded environment variables:")
    for key in ['ENVIRONMENT', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_SCHEMA', 'BOT_NAME', 'DEBUG_MODE']:
        if key in os.environ:
            # Ocultar a senha
            if key == 'DB_PASSWORD':
                print(f"  {key}: ******")
            else:
                print(f"  {key}: {os.environ[key]}")