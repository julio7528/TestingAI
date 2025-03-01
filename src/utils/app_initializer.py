# Application initialization utility
# Este módulo gerencia a inicialização da aplicação, incluindo logger e conexão com banco de dados

import atexit
import os
from dotenv import load_dotenv
from src.utils.db_manager import get_db_manager
from src.utils.logger import EnhancedLogger, ProcessType

# Carrega variáveis de ambiente no início
load_dotenv()

# Variáveis globais para armazenar instâncias
_logger = None
_db_manager = None

def initialize_app():
    """
    Inicializa todos os componentes da aplicação:
    - Carrega variáveis de ambiente
    - Inicializa logger
    - Conecta ao banco de dados
    - Registra função de limpeza ao encerrar
    
    Returns:
        tuple: (logger, db_manager)
    """
    global _logger, _db_manager
    
    # Se já inicializado, retorna as instâncias existentes
    if _logger is not None and _db_manager is not None:
        return _logger, _db_manager
    
    # Inicializa o gerenciador de banco de dados
    _db_manager = get_db_manager()
    
    # Inicializa o logger (isso é feito pelo db_manager)
    _logger = _db_manager.initialize_logging()
    
    # Registra log de início
    _logger.log_info("initialize_app", "Application initialization started", ProcessType.SYSTEM)
    
    # Conecta ao banco de dados
    db_connected = _db_manager.connect()
    
    if db_connected:
        _logger.log_success("initialize_app", "Database connection established", ProcessType.SYSTEM)
    else:
        _logger.log_warning("initialize_app", "Running without database connection", ProcessType.SYSTEM)
    
    # Registra função de limpeza ao encerrar
    atexit.register(cleanup_app)
    
    _logger.log_success("initialize_app", "Application initialized successfully", ProcessType.SYSTEM)
    
    return _logger, _db_manager

def cleanup_app():
    """Limpa recursos ao encerrar a aplicação"""
    global _logger, _db_manager
    
    if _logger is not None:
        _logger.log_info("cleanup_app", "Application shutdown initiated", ProcessType.SYSTEM)
    
    # Fecha conexão com banco de dados
    if _db_manager is not None:
        _db_manager.close()
    
    if _logger is not None:
        _logger.log_info("cleanup_app", "Application shutdown completed", ProcessType.SYSTEM)

def get_logger():
    """Retorna a instância do logger, inicializando a aplicação se necessário"""
    global _logger
    if _logger is None:
        initialize_app()
    return _logger

def get_db_connection():
    """Retorna a conexão com o banco de dados, inicializando a aplicação se necessário"""
    global _db_manager
    if _db_manager is None:
        initialize_app()
    return _db_manager.get_connection()