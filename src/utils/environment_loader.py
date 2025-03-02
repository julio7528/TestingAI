# src/utils/environment_loader.py (updated)
import os
import sys
import argparse

def load_environment():
    """
    Carrega o ambiente correto baseado em argumentos de linha de comando ou variável de ambiente.
    Deve ser chamado antes de qualquer outra importação de configurações.
    
    Returns:
        str: O ambiente carregado ('development' ou 'production')
    """
    # Se já estiver definido, use o valor existente
    if 'ENVIRONMENT' in os.environ:
        env = os.environ['ENVIRONMENT'].lower()
        if env in ['development', 'production']:
            return env
    
    # Procura por argumentos na linha de comando
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--env', dest='environment', 
                        choices=['development', 'production'],
                        help='Set environment (development or production)')
    
    # Tenta fazer o parse, mas ignora erros desconhecidos
    try:
        args, _ = parser.parse_known_args()
        if args.environment:
            os.environ['ENVIRONMENT'] = args.environment
            return args.environment
    except Exception:
        pass
    
    # Valor padrão se nada for especificado
    default_env = 'development'
    os.environ['ENVIRONMENT'] = default_env
    return default_env

# Carrega o ambiente imediatamente quando o módulo é importado
environment = load_environment()
print(f"Environment: {environment}")