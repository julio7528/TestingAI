# src/initializer.py (updated)
# Carrega ambiente primeiro, antes de qualquer outra coisa
from src.utils.environment_loader import environment

# Agora pode importar outros módulos que dependem das configurações
from src.config.settings import Settings
from src.utils.logger import EnhancedLogger
from src.infra.db.db_manager import get_db_manager

# Inicializa componentes globais
settings = Settings()
logger = None
db_manager = None

def initialize_app():
    """
    Inicializa todos os componentes da aplicação:
    - Inicializa logger
    - Conecta ao banco de dados
    - Registra função de limpeza ao encerrar
    
    Returns:
        tuple: (logger, db_manager)
    """
    global logger, db_manager
    
    # Se já inicializado, retorna as instâncias existentes
    if logger is not None and db_manager is not None:
        return logger, db_manager
    
    # Inicializa o gerenciador de banco de dados
    db_manager = get_db_manager()
    
    # Inicializa o logger usando o gerenciador de banco de dados
    logger = db_manager.initialize_logging()
    
    # Registra log de início
    logger.log_info("initialize_app", f"Application initialized with environment: {environment}", "system")
    
    # Conecta ao banco de dados
    db_connected = db_manager.connect()
    
    if db_connected:
        logger.log_success("initialize_app", "Database connection established", "system")
    else:
        logger.log_warning("initialize_app", "Running without database connection", "system")
    
    # Registra função de limpeza ao encerrar
    import atexit
    atexit.register(cleanup_app)
    
    logger.log_success("initialize_app", "Application initialized successfully", "system")
    
    return logger, db_manager

def cleanup_app():
    """Limpa recursos ao encerrar a aplicação"""
    global logger, db_manager
    
    if logger is not None:
        logger.log_info("cleanup_app", "Application shutdown initiated", "system")
    
    # Fecha conexão com banco de dados
    if db_manager is not None:
        db_manager.close()
    
    if logger is not None:
        logger.log_info("cleanup_app", "Application shutdown completed", "system")

# Inicializa a aplicação quando o módulo é importado
logger, db_manager = initialize_app()

# Exporta variáveis importantes
__all__ = ['logger', 'db_manager', 'environment', 'settings']