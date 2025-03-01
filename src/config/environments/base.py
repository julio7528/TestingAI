"""Configurações base compartilhadas por todos os ambientes"""

BASE_SETTINGS = {
    # Informações do projeto
    'PROJECT_INFO': {
        'name': 'rpa_automation',
        'version': '1.0.0',
        'description': 'RPA Automation Framework'
    },

    # Caminhos da aplicação
    'APP_PATHS': {
        'input_folder': 'data/input',
        'output_folder': 'data/output',
        'temp_folder': 'data/temp',
        'logs_folder': 'logs',
        'templates_folder': 'templates'
    },

    # Configurações de processamento padrão
    'SETTINGS': {
        'retry_attempts': 3,
        'timeout_seconds': 30,
    }
}
