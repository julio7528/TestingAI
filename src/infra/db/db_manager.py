# src/infra/db/db_manager.py (updated)
# Database connection manager for RPA

import logging
import psycopg2
from src.config.settings import Settings
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus

# Singleton para gerenciar a conexão com o banco de dados
class DBManager:
    _instance = None
    _connection = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa o gerenciador de banco de dados"""
        self.settings = Settings()
        self._connection = None
        
    def initialize_logging(self):
        """Inicializa o logger antes de conectar ao banco de dados"""
        if DBManager._logger is None:
            proj_name = self.settings.PROJECT_INFO['name'] if hasattr(self.settings, 'PROJECT_INFO') else "rpa_automation"
            DBManager._logger = EnhancedLogger(proj_name)
        return DBManager._logger
    
    def connect(self):
        """Conecta ao banco de dados e retorna o status da conexão"""
        logger = self.initialize_logging()
        
        # Se já estiver conectado, retorna a conexão existente
        if self._connection is not None:
            try:
                # Verifica se a conexão ainda está ativa
                cursor = self._connection.cursor()
                cursor.execute('SELECT 1')
                cursor.close()
                logger.log_info("db_connect", "Using existing database connection", ProcessType.SYSTEM)
                return True
            except Exception:
                # Conexão inativa, fecha para reconectar
                self._connection = None
        
        # Verifica se o banco de dados está habilitado nas configurações
        if not hasattr(self.settings, 'DB_CONFIG') or not self.settings.DB_CONFIG.get('enabled', False):
            logger.log_warning("db_connect", "Database connection disabled in settings", ProcessType.SYSTEM)
            return False
        
        # Conecta ao banco de dados
        try:
            connection_string = self.settings.get_db_connection_string()
            if not connection_string:
                logger.log_error("db_connect", "Invalid database connection string", ProcessType.SYSTEM)
                return False
            
            self._connection = psycopg2.connect(connection_string)
            logger.log_success("db_connect", "Successfully connected to database", ProcessType.SYSTEM)
            
            # Cria a tabela de logs se não existir
            if hasattr(logger, 'connect_to_db'):
                logger.connect_to_db(connection_string)
            
            return True
        except Exception as e:
            logger.log_error("db_connect", f"Failed to connect to database: {str(e)}", ProcessType.SYSTEM)
            return False
    
    def get_connection(self):
        """Retorna a conexão com o banco de dados, tenta reconectar se necessário"""
        if self._connection is None:
            self.connect()
        return self._connection
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self._connection is not None:
            try:
                self._connection.close()
                self._connection = None
                if self._logger:
                    self._logger.log_info("db_close", "Database connection closed", ProcessType.SYSTEM)
                return True
            except Exception as e:
                if self._logger:
                    self._logger.log_error("db_close", f"Error closing database connection: {str(e)}", ProcessType.SYSTEM)
                return False
        return True

# Função para obter a instância singleton do gerenciador de banco de dados
def get_db_manager():
    """Retorna a instância do gerenciador de banco de dados"""
    return DBManager()