# src/bots/bot1/main.py
# Ponto de entrada principal para o bot RPA

import sys
import time
from src.config.settings import Settings
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus
from src.modules.workflow import Workflow
from src.infra.db.db_manager import get_db_manager

def main():
    # Inicializa configurações
    settings = Settings()
    
    # Inicializa logger
    logger = EnhancedLogger(settings.PROJECT_INFO['name'])
    logger.debug_mode = settings.SETTINGS['debug_mode']
    
    # Inicializa conexão com banco de dados (se habilitado)
    if settings.DB_CONFIG['enabled']:
        db_manager = get_db_manager()
        db_manager._logger = logger  # Associa o logger com o DB manager
        db_connected = db_manager.connect()
        if db_connected:
            logger.log_success("main", "Conexão com banco de dados estabelecida", ProcessType.SYSTEM)
        else:
            logger.log_warning("main", "Executando sem conexão com banco de dados", ProcessType.SYSTEM)
    
    # Log de início do processo RPA
    logger.log_info("main", f"Iniciando processo RPA em ambiente {settings.ENVIRONMENT.upper()}", ProcessType.ROBOTIC)
    logger.log_info("main", f"Bot: {settings.BOT_NAME}", ProcessType.SYSTEM)
    
    try:
        # Execução do workflow
        logger.log_info("main", "Inicializando workflow", ProcessType.ROBOTIC)
        workflow = Workflow()
        
        # Etapa 1: Extração de dados
        logger.log_info("main", "Iniciando extração de dados", ProcessType.BUSINESS)
        workflow.step1_data_extraction()
        logger.log_success("main", "Extração de dados concluída", ProcessType.BUSINESS)
        
        # Etapa 2: Transformação de dados
        logger.log_info("main", "Iniciando transformação de dados", ProcessType.BUSINESS)
        workflow.step2_data_transformation()
        logger.log_success("main", "Transformação de dados concluída", ProcessType.BUSINESS)
        
        # Etapa 3: Carregamento de dados
        logger.log_info("main", "Iniciando carregamento de dados", ProcessType.BUSINESS)
        workflow.step3_data_loading()
        logger.log_success("main", "Carregamento de dados concluído", ProcessType.BUSINESS)
        
        # Workflow completo
        result = workflow.execute_workflow()
        logger.log_success("main", f"Workflow concluído com status: {result['status']}", ProcessType.PROCESS)
        
    except Exception as e:
        logger.log_critical("main", f"Erro crítico no processo RPA: {str(e)}", ProcessType.SYSTEM)
        return 1
    
    logger.log_info("main", "Processo RPA concluído com sucesso", ProcessType.ROBOTIC)
    return 0

if __name__ == '__main__':
    sys.exit(main())