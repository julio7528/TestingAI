# Main entry point for the RPA bot

import sys
import time
from src.modules.workflow import Workflow
from src.utils.app_initializer import initialize_app

def main():
    # Inicializa a aplicação (logger e conexão com banco de dados)
    logger, _ = initialize_app()
    
    # Log de início do processo RPA
    logger.log_info("main", "Starting RPA process", process_type="robotic")
    
    try:
        # Example workflow execution
        logger.log_info("main", "Initializing workflow", process_type="robotic")
        workflow = Workflow()
        
        # Step 1: Data Extraction
        logger.log_info("main", "Starting data extraction", process_type="business")
        workflow.step1_data_extraction()
        logger.log_success("main", "Data extraction completed", process_type="business")
        
        # Step 2: Data Transformation
        logger.log_info("main", "Starting data transformation", process_type="business")
        workflow.step2_data_transformation()
        logger.log_success("main", "Data transformation completed", process_type="business")
        
        # Step 3: Data Loading
        logger.log_info("main", "Starting data loading", process_type="business")
        workflow.step3_data_loading()
        logger.log_success("main", "Data loading completed", process_type="business")
        
        # Complete workflow
        result = workflow.execute_workflow()
        logger.log_success("main", f"Workflow completed with status: {result['status']}", process_type="process")
        
    except Exception as e:
        logger.log_critical("main", f"Critical error in RPA process: {str(e)}", process_type="system")
        return 1
    
    logger.log_info("main", "RPA process completed successfully", process_type="robotic")
    return 0

if __name__ == '__main__':
    sys.exit(main())