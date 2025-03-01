import os
"""Configurações específicas do ambiente de produção"""


PRODUCTION_SETTINGS = {
    # Modo debug desativado em produção
    'DEBUG': False,
    
    # Configuração de banco de dados
    'DB_CONFIG': {
        'enabled': True,
        'host': os.getenv('DB_HOST', 'db.production.example.com'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'rpa_prod'),
        'user': os.getenv('DB_USER', 'rpa_user'),
        'password': os.getenv('DB_PASSWORD', '')  # Sempre buscar do ambiente em produção
    },
    
    # Configurações ajustadas para produção
    'SETTINGS': {
        'retry_attempts': 3,
        'timeout_seconds': 30,
        'debug_mode': False
    },
    
    # Configurações de email para produção
    'EMAIL_CONFIG': {
        'enabled': True,
        'send_to_real_recipients': True,
    }
}
