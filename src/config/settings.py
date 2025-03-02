# src/config/settings.py
import os
import sys
from dotenv import load_dotenv

# Certifique-se de que as variáveis de ambiente estão carregadas
from src.utils.environment_loader import environment

class Settings:
    """
    Configurações centralizadas para a solução RPA.
    Carrega configurações de variáveis de ambiente e valores padrão.
    """
    
    def __init__(self):
        # Ambiente atual (já definido pelo environment_loader)
        self.ENVIRONMENT = environment
        
        # Nome do bot (usado por vários módulos)
        self.BOT_NAME = os.getenv('BOT_NAME', 'ModelViewer')
        
        # Informações do projeto
        self.PROJECT_INFO = {
            'name': os.getenv('PROJECT_NAME', 'rpa_automation'),
            'version': os.getenv('PROJECT_VERSION', '1.0.0'),
            'description': 'RPA Automation Framework'
        }

        # Caminhos da aplicação
        self.APP_PATHS = {
            'input_folder': os.getenv('INPUT_FOLDER', 'data/input'),
            'output_folder': os.getenv('OUTPUT_FOLDER', 'data/output'),
            'temp_folder': os.getenv('TEMP_FOLDER', 'data/temp'),
            'logs_folder': os.getenv('LOGS_FOLDER', 'logs')
        }

        # Configurações de processamento
        self.SETTINGS = {
            'retry_attempts': int(os.getenv('APP_RETRY_ATTEMPTS', 3)),
            'timeout_seconds': int(os.getenv('APP_TIMEOUT_SECONDS', 30)),
            'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() in ('true', '1', 'yes')
        }

        # Configurações de banco de dados - carregadas diretamente do .env
        self.DB_CONFIG = {
            'enabled': True,  # Por padrão vamos assumir que DB está habilitado
            'host': os.getenv('DB_HOST', ''),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', ''),
            'password': os.getenv('DB_PASSWORD', ''),
            'schema': os.getenv('DB_SCHEMA', self.PROJECT_INFO['name'])
        }

        # Validar configurações de DB
        if not self.DB_CONFIG['host'] or not self.DB_CONFIG['user'] or not self.DB_CONFIG['password']:
            self.DB_CONFIG['enabled'] = False
            
        # Exibe configurações de inicialização se em modo debug
        if self.SETTINGS['debug_mode']:
            self._print_settings_summary()

    def get_db_connection_string(self):
        """Gera string de conexão PostgreSQL a partir das configurações"""
        if not self.DB_CONFIG['enabled']:
            return None
        return f"postgresql://{self.DB_CONFIG['user']}:{self.DB_CONFIG['password']}@{self.DB_CONFIG['host']}:{self.DB_CONFIG['port']}/{self.DB_CONFIG['database']}"
    
    def _print_settings_summary(self):
        """Exibe um resumo das configurações carregadas"""
        print("\n" + "="*50)
        print(f"RPA AUTOMATION - AMBIENTE: {self.ENVIRONMENT.upper()}")
        print("="*50)
        print(f"Projeto: {self.PROJECT_INFO['name']} v{self.PROJECT_INFO['version']}")
        print(f"Bot: {self.BOT_NAME}")
        print(f"Debug: {'Ativado' if self.SETTINGS['debug_mode'] else 'Desativado'}")
        print(f"Banco de Dados: {'Configurado' if self.DB_CONFIG['enabled'] else 'Desativado'}")
        if self.DB_CONFIG['enabled']:
            print(f"  - Host: {self.DB_CONFIG['host']}")
            print(f"  - Banco: {self.DB_CONFIG['database']}")
            print(f"  - Usuário: {self.DB_CONFIG['user']}")
            print(f"  - Schema: {self.DB_CONFIG['schema']}")
        print("="*50 + "\n")