import os
import sys
import argparse

def load_environment():
    """
    Carrega o ambiente correto baseado em argumentos de linha de comando ou variável de ambiente.
    Deve ser chamado antes de qualquer outra importação de configurações.
    """
    # Verifica se já existe variável de ambiente definida
    if 'ENVIRONMENT' in os.environ:
        return os.environ['ENVIRONMENT']
    
    # Se não, procura por argumentos na linha de comando
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--env' and i < len(sys.argv):
            env = sys.argv[i+1]
            if env in ['development', 'production']:
                os.environ['ENVIRONMENT'] = env
                return env
        elif arg.startswith('--env='):
            env = arg.split('=')[1]
            if env in ['development', 'production']:
                os.environ['ENVIRONMENT'] = env
                return env
    
    # Valor padrão se nada for especificado
    default_env = 'development'
    os.environ['ENVIRONMENT'] = default_env
    return default_env

# Carrega o ambiente imediatamente quando o módulo é importado
environment = load_environment()