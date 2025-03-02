# src/bots/template/main.py
# Template padronizado para os bots RPA

import sys
import time
import traceback

# Inicializa a aplicação (carrega ambiente, configurações, logger e DB)
from src.initializer import initialize_app, settings

# Importa módulos comuns
from src.modules.workflow import Workflow
from src.utils.logger import ProcessType, LogStatus

def main():
    """
    Ponto de entrada principal do bot RPA.
    Gerencia o fluxo de execução e tratamento de erros.
    """
    # Inicializa a aplicação (obtém logger e db_manager)
    logger, db_manager = initialize_app()
    
    # Log de início
    logger.log_info("main", f"Iniciando processo RPA no ambiente {settings.ENVIRONMENT.upper()}", ProcessType.ROBOTIC)
    logger.log_info("main", f"Bot: {settings.BOT_NAME}", ProcessType.SYSTEM)
    
    try:
        # Execução do workflow principal
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
        
        # Executa o workflow completo
        result = workflow.execute_workflow()
        logger.log_success("main", f"Workflow concluído com status: {result['status']}", ProcessType.PROCESS)
        
    except Exception as e:
        # Captura e registra detalhes do erro
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        logger.log_critical("main", f"Erro crítico no processo RPA: {error_message}", ProcessType.SYSTEM)
        
        # Registra o traceback em modo debug
        if settings.SETTINGS['debug_mode']:
            logger.log_error("main", f"Traceback: {error_traceback}", ProcessType.SYSTEM)
        
        # Aqui você pode adicionar notificações (email, Slack, etc)
        
        return 1  # Código de erro
    
    logger.log_info("main", "Processo RPA concluído com sucesso", ProcessType.ROBOTIC)
    return 0  # Código de sucesso

if __name__ == '__main__':
    sys.exit(main())