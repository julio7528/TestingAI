# Enhanced logging utility with text file and database support

import logging
import os
import time
import datetime
import inspect
import psutil
import psycopg2
import textwrap
from enum import Enum
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

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
        self.log_dir = os.path.join(os.getcwd(), 'logs')  # Usa o diretório atual + /logs
        self.log_file = None
        self.db_connection = None
        self.debug_mode = True  # Valor padrão
        self.bot_name = os.getenv('BOT_NAME', 'Default Bot')  # Usa a variável de ambiente ou valor padrão
        self.separator_line = "+---------------------+---------------+------------------------------+-------------------------+-------+-------+--------------------------------------------------+---------------+-------------+"
        self.message_width = 48  # Largura máxima da coluna de mensagem
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f"rpa_{self.project_name}_{timestamp}.log")
        
        # Create formatted header for the log file with better visual separation
        self._write_formatted_header()
        
        # Set up standard Python logging
        logging.basicConfig(
            level=logging.DEBUG if self.debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        # Register function to add closing line on program exit
        import atexit
        atexit.register(self._add_closing_line)

    def _write_formatted_header(self):
        """Write a formatted header to the log file"""
        # Define columns with fixed widths for better alignment
        columns = [
            "TIMESTAMP", "TASK", "FUNCTION", "FILE", "CPU%", "MEM%", 
            "MESSAGE", "PROCESS_TYPE", "STATUS"
        ]
        
        # Create a visually appealing header with consistent borders and spacing
        header_line = "| {:<19} | {:<13} | {:<28} | {:<23} | {:<5} | {:<5} | {:<48} | {:<13} | {:<11} |".format(*columns)
        
        with open(self.log_file, 'w') as f:
            f.write(f"{self.separator_line}\n")
            f.write(f"{header_line}\n")
            f.write(f"{self.separator_line}\n")

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
            
            # Create logs table with the new source_file column
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.project_name}.logs (
                id SERIAL PRIMARY KEY,
                task_name VARCHAR(255),
                function_name VARCHAR(255),
                source_file VARCHAR(255),  -- New column for source file
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
    
    def _get_caller_info(self, depth=3):
        """Get information about the caller (file, function)
        
        Args:
            depth (int): How far back in the stack to look for the caller
                       2 = the direct caller of this method
                       3 = the caller of the logging method (default)
                       4 or more = further back in the call stack
        
        Returns:
            tuple: (filename, function_name)
        """
        try:
            # Pega a stack de chamadas até o depth desejado
            frame = inspect.currentframe()
            for _ in range(depth):
                if frame.f_back is None:
                    break
                frame = frame.f_back
            
            # Extrai informações do frame
            if frame:
                frame_info = inspect.getframeinfo(frame)
                filename = os.path.basename(frame_info.filename)
                function_name = frame_info.function
                return filename, function_name
        except Exception:
            pass
        
        return "unknown.py", "unknown"
    
    def log_entry(self, function_name, log_message, process_type=ProcessType.SYSTEM, status=LogStatus.INFO, task_name=None, extra_data=None):
        """Log a new entry to both file and database"""
        # Get system usage stats
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        # Get current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        log_date = now.strftime('%Y-%m-%d')
        log_time = now.strftime('%H:%M:%S')
        
        # Use task_name from environment variable if not provided
        if task_name is None:
            task_name = self.bot_name
        
        # Get caller info (file) - obtenha apenas o arquivo, o nome da função já é fornecido
        source_file, _ = self._get_caller_info(depth=3)
        
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
        
        # Format status
        status_str = status.value
        
        # Wrap long messages
        message_lines = self._wrap_message(log_message)
        
        # Write first line with full information
        log_entry = "| {:<19} | {:<13} | {:<28} | {:<23} | {:<5.1f} | {:<5.1f} | {:<48} | {:<13} | {:<11} |".format(
            timestamp, task_name, function_name, source_file, 
            cpu_usage, memory_usage, 
            message_lines[0], 
            process_type.value, status_str
        )
        
        with open(self.log_file, 'a') as f:
            f.write(f"{log_entry}\n")
            
            # Write continuation lines for long messages
            if len(message_lines) > 1:
                continuation_prefix = "|" + " " * 111
                for i in range(1, len(message_lines)):
                    cont_line = f"{continuation_prefix}{message_lines[i]:<48} |" + " " * 27 + "|"
                    f.write(f"{cont_line}\n")
            
            # Add a separator after critical errors for emphasis
            if status == LogStatus.CRITICAL:
                f.write(f"{self.separator_line}\n")
        
        # Log to console
        log_level = self._get_log_level(status)
        logging.log(log_level, f"{task_name} - {function_name}: {log_message}")
        
        # Save to database if connected
        self._log_to_database(task_name, function_name, source_file, cpu_usage, memory_usage, 
                            log_date, log_time, log_message, process_type, status, extra_data)
    
    def _wrap_message(self, message):
        """Wrap message text to fit within column width"""
        return textwrap.wrap(message, width=self.message_width)
        
    def _add_closing_line(self):
        """Add closing line to log file on program exit"""
        if hasattr(self, 'log_file') and self.log_file and os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"{self.separator_line}\n")
            except Exception:
                pass  # Silently fail if we can't write to the file
                            
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
    
    def _log_to_database(self, task_name, function_name, source_file, cpu_usage, memory_usage, 
                        log_date, log_time, log_message, process_type, status, extra_data):
        """Save log entry to database"""
        if not self.db_connection:
            return
            
        try:
            cursor = self.db_connection.cursor()
            
            sql = f"""
            INSERT INTO {self.project_name}.logs 
            (task_name, function_name, source_file, cpu_usage, memory_usage, log_date, log_time, 
            log_message, process_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(
                sql,
                (task_name, function_name, source_file, cpu_usage, memory_usage, log_date, log_time, 
                log_message, process_type, status)
            )
            
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            logging.error(f"Failed to log to database: {e}")
    
    def log_info(self, function_name, message, process_type=ProcessType.SYSTEM):
        """Log information message"""
        self.log_entry(function_name, message, process_type, LogStatus.INFO)
    
    def log_success(self, function_name, message, process_type=ProcessType.SYSTEM):
        """Log success message"""
        self.log_entry(function_name, message, process_type, LogStatus.SUCCESS)
    
    def log_warning(self, function_name, message, process_type=ProcessType.SYSTEM):
        """Log warning message"""
        self.log_entry(function_name, message, process_type, LogStatus.WARNING)
    
    def log_error(self, function_name, message, process_type=ProcessType.SYSTEM):
        """Log error message"""
        self.log_entry(function_name, message, process_type, LogStatus.FAILURE)
    
    def log_critical(self, function_name, message, process_type=ProcessType.SYSTEM):
        """Log critical error message"""
        self.log_entry(function_name, message, process_type, LogStatus.CRITICAL)