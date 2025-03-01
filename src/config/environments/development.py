import os
"""Configurações específicas do ambiente de desenvolvimento"""

DEVELOPMENT_SETTINGS = {
    # Modo debug ativado em desenvolvimento
    'DEBUG': True,
    
    # Configuração de banco de dados
    'DB_CONFIG': {
        'enabled': True,
        'host': 'localhost',
        'port': '5432',
        'database': 'rpa_dev',
        'user': 'postgres',
        'password': os.getenv('DB_PASSWORD', 'dev_password')
    },
    
    # Configurações específicas de desenvolvimento
    'SETTINGS': {
        'retry_attempts': 5,  # Mais tentativas em desenvolvimento
        'timeout_seconds': 60,  # Timeout maior para debugging
        'debug_mode': True
    },
    
    # Configurações de email para desenvolvimento
    'EMAIL_CONFIG': {
        'enabled': True,
        'send_to_real_recipients': False,  # Em dev, não envia para destinatários reais
        'test_recipients': ['dev@example.com'],  # Lista de emails para teste
    }
}