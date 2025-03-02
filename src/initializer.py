# src/initializer.py
# Inicializador central da aplicação

# Importa o ambiente primeiro (isso carrega as variáveis de ambiente do .env)
from src.utils.environment_loader import environment

# Depois importa os outros módulos que dependem das variáveis de ambiente
from src.config.settings import Settings
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus
from src.infra.db.db_manager import get_db_manager
import atexit

# Variáveis globais
settings = Settings()
logger = None
db_manager = None

def cleanup_app():
    """Limpa recursos ao encerrar a aplicação"""
    global logger, db_manager
    
    if logger:
        logger.log_info("cleanup_app", "Finalizando aplicação...", ProcessType.SYSTEM)
    
    # Fecha conexão com banco de dados
    if db_manager:
        db_manager.close()
    
    if logger:
        logger.log_info("cleanup_app", "Aplicação finalizada com sucesso", ProcessType.SYSTEM)

def initialize_app():
    """
    Inicializa todos os componentes da aplicação:
    - Configura o logger
    - Conecta ao banco de dados
    - Registra função de limpeza ao encerrar
    
    Returns:
        tuple: (logger, db_manager)
    """
    global logger, db_manager
    
    # Se já inicializado, retorna as instâncias existentes
    if logger is not None and db_manager is not None:
        return logger, db_manager
    
    # Inicializa o DB Manager
    db_manager = get_db_manager()
    
    # Inicializa o logger
    logger = db_manager.initialize_logging()
    
    # Ajusta modo de debug conforme configurações
    logger.debug_mode = settings.SETTINGS['debug_mode']
    
    # Log inicial
    logger.log_info("initialize_app", f"Inicializando aplicação no ambiente: {environment}", ProcessType.SYSTEM)
    
    # Conecta ao banco de dados
    db_connected = db_manager.connect()
    
    if db_connected:
        logger.log_success("initialize_app", "Conexão com banco de dados estabelecida", ProcessType.SYSTEM)
        # Conecta o logger ao banco de dados
        connection = db_manager.get_connection()
        if connection:
            logger.connect_to_db(connection)
            logger.log_success("initialize_app", "Logger conectado ao banco de dados", ProcessType.SYSTEM)
    else:
        logger.log_warning("initialize_app", "Executando sem conexão com banco de dados", ProcessType.SYSTEM)
    
    # Registra função de limpeza
    atexit.register(cleanup_app)
    
    logger.log_success("initialize_app", "Aplicação inicializada com sucesso", ProcessType.SYSTEM)
    
    return logger, db_manager

# Exporta variáveis importantes
__all__ = ['initialize_app', 'logger', 'db_manager', 'settings', 'environment']