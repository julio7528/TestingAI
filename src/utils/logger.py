# Enhanced logging utility with text file and database support

import logging
import os
import time
import datetime
import psutil
import psycopg2
from enum import Enum

class ProcessType(str, Enum):
    ROBOTIC = "robotic"
    BUSINESS = "business"
    SYSTEM = "system"
    PROCESS = "process"

class LogStatus(str, Enum):
    FAILURE = "failure"
    SUCCESS = "success"
    WARNING = "warning"
    CRITICAL = "critical"
    INFO = "information"

class EnhancedLogger:
    def __init__(self, project_name):
        self.project_name = project_name
        # Como não estamos mais importando settings diretamente
        # vamos passar como parâmetro ou buscar de outro lugar
        self.log_dir = 'logs'
        self.log_file = None
        self.db_connection = None
        self.debug_mode = True  # Valor padrão
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f"rpa_{self.project_name}_{timestamp}.log")
        
        # Create column headers for the log file
        headers = "task_name|function_name|cpu_usage|memory_usage|date|time|log_message|process_type|status"
        
        with open(self.log_file, 'w') as f:
            f.write(f"{headers}\n")
        
        # Set up standard Python logging
        logging.basicConfig(
            level=logging.DEBUG if self.debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )

    def connect_to_db(self, connection_string):
        """Connect to PostgreSQL database"""
        try:
            self.db_connection = psycopg2.connect(connection_string)
            self.create_log_table_if_not_exists()
            return True
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
            return False
    
    def create_log_table_if_not_exists(self):
        """Create log table in the database if it doesn't exist"""
        if not self.db_connection:
            return False
        
        try:
            cursor = self.db_connection.cursor()
            
            # Create schema if it doesn't exist
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {self.project_name}")
            
            # Create logs table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.project_name}.logs (
                id SERIAL PRIMARY KEY,
                task_name VARCHAR(255),
                function_name VARCHAR(255),
                cpu_usage FLOAT,
                memory_usage FLOAT,
                log_date DATE,
                log_time TIME,
                log_message TEXT,
                process_type VARCHAR(50),
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_sql)
            self.db_connection.commit()
            cursor.close()
            return True
        except Exception as e:
            logging.error(f"Failed to create log table: {e}")
            return False
    
    def log_entry(self, task_name, function_name, log_message, process_type, status, extra_data=None):
        """Log a new entry to both file and database"""
        # Get system usage stats
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        # Get current date and time
        now = datetime.datetime.now()
        log_date = now.strftime('%Y-%m-%d')
        log_time = now.strftime('%H:%M:%S')
        
        # Validate enum values
        if not isinstance(process_type, ProcessType):
            try:
                process_type = ProcessType(process_type.lower())
            except ValueError:
                process_type = ProcessType.SYSTEM
                
        if not isinstance(status, LogStatus):
            try:
                status = LogStatus(status.lower())
            except ValueError:
                status = LogStatus.INFO
        
        # Create log entry
        log_entry = f"{task_name}|{function_name}|{cpu_usage}|{memory_usage}|{log_date}|{log_time}|{log_message}|{process_type}|{status}"
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(f"{log_entry}\n")
        
        # Log to console
        log_level = self._get_log_level(status)
        logging.log(log_level, f"{task_name} - {function_name}: {log_message}")
        
        # Save to database if connected
        self._log_to_database(task_name, function_name, cpu_usage, memory_usage, 
                            log_date, log_time, log_message, process_type, status, extra_data)
                            
    def _get_log_level(self, status):
        """Map log status to Python logging level"""
        status_map = {
            LogStatus.CRITICAL: logging.CRITICAL,
            LogStatus.FAILURE: logging.ERROR,
            LogStatus.WARNING: logging.WARNING,
            LogStatus.INFO: logging.INFO,
            LogStatus.SUCCESS: logging.INFO
        }
        return status_map.get(status, logging.INFO)
    
    def _log_to_database(self, task_name, function_name, cpu_usage, memory_usage, 
                        log_date, log_time, log_message, process_type, status, extra_data):
        """Save log entry to database"""
        if not self.db_connection:
            return
            
        try:
            cursor = self.db_connection.cursor()
            
            sql = f"""
            INSERT INTO {self.project_name}.logs 
            (task_name, function_name, cpu_usage, memory_usage, log_date, log_time, 
            log_message, process_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(
                sql,
                (task_name, function_name, cpu_usage, memory_usage, log_date, log_time, 
                log_message, process_type, status)
            )
            
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            logging.error(f"Failed to log to database: {e}")
    
    def log_info(self, task_name, function_name, message, process_type=ProcessType.SYSTEM):
        """Log information message"""
        self.log_entry(task_name, function_name, message, process_type, LogStatus.INFO)
    
    def log_success(self, task_name, function_name, message, process_type=ProcessType.SYSTEM):
        """Log success message"""
        self.log_entry(task_name, function_name, message, process_type, LogStatus.SUCCESS)
    
    def log_warning(self, task_name, function_name, message, process_type=ProcessType.SYSTEM):
        """Log warning message"""
        self.log_entry(task_name, function_name, message, process_type, LogStatus.WARNING)
    
    def log_error(self, task_name, function_name, message, process_type=ProcessType.SYSTEM):
        """Log error message"""
        self.log_entry(task_name, function_name, message, process_type, LogStatus.FAILURE)
    
    def log_critical(self, task_name, function_name, message, process_type=ProcessType.SYSTEM):
        """Log critical error message"""
        self.log_entry(task_name, function_name, message, process_type, LogStatus.CRITICAL)