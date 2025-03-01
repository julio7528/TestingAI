# Main entry point for the RPA bot

import sys
import time
from src.config.settings import Settings
from src.modules import data_handler
from src.modules.workflow import Workflow
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus

def main():
    # Inicializa as configurações
    settings = Settings()
    
    # Initialize the enhanced logger
    logger = EnhancedLogger(settings.PROJECT_INFO['name'])
    logger.log_info("Main Bot", "main", "Starting RPA process", ProcessType.ROBOTIC)
    
    # Connect to database if enabled
    if settings.DB_CONFIG['enabled']:
        connection_string = settings.get_db_connection_string()
        if connection_string:
            db_connected = logger.connect_to_db(connection_string)
            if db_connected:
                logger.log_info("Main Bot", "main", "Successfully connected to database", ProcessType.SYSTEM)
            else:
                logger.log_warning("Main Bot", "main", "Failed to connect to database, continuing with file logging only", ProcessType.SYSTEM)
    
    try:
        # Example workflow execution
        logger.log_info("Main Bot", "main", "Initializing workflow", ProcessType.ROBOTIC)
        workflow = Workflow()
        
        # Step 1: Data Extraction
        logger.log_info("Main Bot", "step1_data_extraction", "Starting data extraction", ProcessType.BUSINESS)
        workflow.step1_data_extraction()
        logger.log_success("Main Bot", "step1_data_extraction", "Data extraction completed", ProcessType.BUSINESS)
        
        # Step 2: Data Transformation
        logger.log_info("Main Bot", "step2_data_transformation", "Starting data transformation", ProcessType.BUSINESS)
        workflow.step2_data_transformation()
        logger.log_success("Main Bot", "step2_data_transformation", "Data transformation completed", ProcessType.BUSINESS)
        
        # Step 3: Data Loading
        logger.log_info("Main Bot", "step3_data_loading", "Starting data loading", ProcessType.BUSINESS)
        workflow.step3_data_loading()
        logger.log_success("Main Bot", "step3_data_loading", "Data loading completed", ProcessType.BUSINESS)
        
        # Complete workflow
        result = workflow.execute_workflow()
        logger.log_success("Main Bot", "execute_workflow", f"Workflow completed with status: {result['status']}", ProcessType.PROCESS)
        
    except Exception as e:
        logger.log_critical("Main Bot", "main", f"Critical error in RPA process: {str(e)}", ProcessType.SYSTEM)
        return 1
    
    logger.log_info("Main Bot", "main", "RPA process completed successfully", ProcessType.ROBOTIC)
    return 0

if __name__ == '__main__':
    sys.exit(main())