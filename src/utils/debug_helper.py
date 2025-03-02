# src/utils/debug_helper.py
"""
Módulo auxiliar para facilitar o debug no VSCode
"""

import os
import sys
import inspect

def debug_info():
    """
    Exibe informações úteis para debug
    """
    print("\n" + "="*50)
    print("INFORMAÇÕES DE DEBUG")
    print("="*50)
    
    # Ambiente
    print(f"Ambiente: {os.getenv('ENVIRONMENT', 'não definido')}")
    
    # Diretório de trabalho
    print(f"Diretório atual: {os.getcwd()}")
    
    # Caminho do Python
    print(f"Executável Python: {sys.executable}")
    
    # Variáveis de ambiente
    print("\nVariáveis de ambiente relevantes:")
    env_vars = ['ENVIRONMENT', 'DB_HOST', 'DB_NAME', 'DEBUG_MODE', 'BOT_NAME']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Oculta senhas e informações sensíveis
            if var in ['DB_PASSWORD']:
                value = '****'
            print(f"  {var}: {value}")
    
    print("="*50)
    return True

def caller_info():
    """
    Retorna informações sobre o chamador para debugging
    """
    caller_frame = inspect.currentframe().f_back
    if caller_frame:
        caller_info = inspect.getframeinfo(caller_frame)
        return {
            'file': caller_info.filename,
            'function': caller_info.function,
            'line': caller_info.lineno,
            'code': caller_info.code_context[0].strip() if caller_info.code_context else None
        }
    return None

def interactive_debug():
    """
    Ponto de pausa para debug interativo
    Coloque um breakpoint aqui para depurar interativamente
    """
    caller = caller_info()
    print(f"\nPONTO DE DEBUG INTERATIVO")
    if caller:
        print(f"Chamado de: {caller['file']}")
        print(f"Função: {caller['function']}, Linha: {caller['line']}")
        if caller['code']:
            print(f"Código: {caller['code']}")
    
    # Esta linha é ideal para colocar um breakpoint
    debug_breakpoint = True  # Coloque o breakpoint nesta linha
    
    return debug_breakpoint