# src/infra/db/db_manager.py
import logging
import psycopg2
from src.config.settings import Settings
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus

class DBManager:
    """
    Singleton para gerenciar a conexão com o banco de dados.
    Responsável por estabelecer e manter a conexão com o Supabase.
    """
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
        if not DBManager._logger:
            proj_name = self.settings.PROJECT_INFO['name']
            DBManager._logger = EnhancedLogger(proj_name)
            DBManager._logger.debug_mode = self.settings.SETTINGS['debug_mode']
        return DBManager._logger
    
    def connect(self):
        """Conecta ao banco de dados Supabase e retorna o status da conexão"""
        logger = self.initialize_logging()
        
        # Se já estiver conectado, verifica se a conexão ainda está ativa
        if self._connection:
            try:
                cursor = self._connection.cursor()
                cursor.execute('SELECT 1')
                cursor.close()
                logger.log_info("db_connect", "Usando conexão existente com o banco de dados", ProcessType.SYSTEM)
                return True
            except Exception:
                # Conexão inativa, fecha para reconectar
                self._connection = None
                logger.log_warning("db_connect", "Conexão perdida, tentando reconectar", ProcessType.SYSTEM)
        
        # Verifica se o banco de dados está habilitado nas configurações
        if not self.settings.DB_CONFIG['enabled']:
            logger.log_warning("db_connect", "Conexão com banco de dados desabilitada nas configurações", ProcessType.SYSTEM)
            return False
        
        # Tenta estabelecer a conexão com o Supabase
        try:
            # Pega os dados de conexão das configurações
            db_config = self.settings.DB_CONFIG
            
            # Log dos parâmetros de conexão (sem senha)
            if self.settings.SETTINGS['debug_mode']:
                logger.log_info("db_connect", 
                               f"Tentando conectar ao banco: {db_config['host']}:{db_config['port']}/{db_config['database']} "
                               f"com usuário {db_config['user']}", 
                               ProcessType.SYSTEM)
            
            # Estabelece a conexão
            self._connection = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            # Testando a conexão
            cursor = self._connection.cursor()
            cursor.execute('SELECT version()')
            version = cursor.fetchone()[0]
            cursor.close()
            
            logger.log_success("db_connect", f"Conectado com sucesso ao Supabase: {version}", ProcessType.SYSTEM)
            
            # Configura o schema se necessário
            if db_config.get('schema'):
                cursor = self._connection.cursor()
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {db_config['schema']}")
                self._connection.commit()
                cursor.close()
                logger.log_success("db_connect", f"Schema '{db_config['schema']}' verificado/criado", ProcessType.SYSTEM)
            
            # Cria a tabela de logs se o logger precisar
            if hasattr(logger, 'connect_to_db'):
                logger.connect_to_db(self._connection)
            
            return True
        except Exception as e:
            error_msg = str(e)
            logger.log_error("db_connect", f"Falha ao conectar ao banco de dados: {error_msg}", ProcessType.SYSTEM)
            return False
    
    def get_connection(self):
        """Retorna a conexão ativa ou tenta reconectar"""
        if not self._connection:
            self.connect()
        return self._connection
    
    def execute_query(self, query, params=None, commit=False):
        """
        Executa uma query no banco de dados
        
        Args:
            query (str): Query SQL a ser executada
            params (tuple, optional): Parâmetros para a query
            commit (bool, optional): Se deve fazer commit após a execução
            
        Returns:
            tuple: (success, result/error_message)
        """
        logger = self.initialize_logging()
        
        if not self._connection and not self.connect():
            return False, "Não foi possível conectar ao banco de dados"
        
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            
            if commit:
                self._connection.commit()
                result = cursor.rowcount
            else:
                result = cursor.fetchall()
                
            cursor.close()
            return True, result
        except Exception as e:
            error_msg = str(e)
            logger.log_error("execute_query", f"Erro ao executar query: {error_msg}", ProcessType.SYSTEM)
            return False, error_msg
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        logger = self.initialize_logging()
        
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                logger.log_info("db_close", "Conexão com banco de dados fechada", ProcessType.SYSTEM)
                return True
            except Exception as e:
                logger.log_error("db_close", f"Erro ao fechar conexão: {str(e)}", ProcessType.SYSTEM)
                return False
        return True

# Função para obter a instância singleton do gerenciador de banco de dados
def get_db_manager():
    """Retorna a instância do gerenciador de banco de dados"""
    return DBManager()