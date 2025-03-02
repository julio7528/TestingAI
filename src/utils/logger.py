# Modificação completa para o arquivo src/utils/logger.py
# Foco no alinhamento exato do cabeçalho e separadores

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
        
        # Formato de colunas - definições de largura
        self.col_widths = {
            'timestamp': 25,    # TIMESTAMP
            'task': 15,         # TASK
            'function': 30,     # FUNCTION
            'file': 25,         # FILE
            'message': 50,      # MESSAGE
            'process_type': 15, # PROCESS_TYPE
            'status': 15        # STATUS
        }
        
        # Largura para wrap de mensagens
        self.message_width = self.col_widths['message']
        
        # Quantidade de espaço entre borda e conteúdo da coluna
        self.padding = 1
        
        # Setup inicial
        self.setup_logging()
        
    def setup_logging(self):
        """Configuração inicial do logging"""
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f"rpa_{self.project_name}_{timestamp}.log")
        
        # Define UTF-8 encoding for the log file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            # Escreve o cabeçalho do arquivo de log
            f.write(self._create_header())
        
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
        
    def _create_separator_line(self):
        """Cria a linha separadora com + alinhado precisamente com as barras verticais"""
        separator = "+"
        for name, width in self.col_widths.items():
            # Adiciona dois traços extras para compensar o espaço de padding em cada lado
            separator += "-" * (width + self.padding * 2) + "+"
        return separator
        
    def _create_header(self):
        """Cria o cabeçalho com alinhamento preciso e títulos melhor centralizados"""
        # Títulos das colunas com um espaço adicional em cada lado para melhor centralização
        headers = {
            'timestamp': " TIMESTAMP ",
            'task': " TASK ",
            'function': " FUNCTION ",
            'file': " FILE ",
            'message': " MESSAGE ",
            'process_type': " PROCESS_TYPE ",
            'status': " STATUS "
        }
        
        # Criar linha separadora
        separator = self._create_separator_line()
        
        # Criar linha de cabeçalho
        header_line = "|"
        for name, width in self.col_widths.items():
            # Centraliza o título na coluna
            title = headers[name]
            padding_left = self.padding + (width - len(title) + 1) // 2  # +2 para compensar os espaços adicionados
            padding_right = width - (len(title) - 1) - padding_left + self.padding  # -2 para compensar os espaços adicionados
            header_line += " " * padding_left + title + " " * padding_right + "|"
        
        # Monta o cabeçalho completo
        full_header = separator + "\n" + header_line + "\n" + separator + "\n"
        return full_header

    def connect_to_db(self, connection):
        """Connect to PostgreSQL database
        
        Args:
            connection: Can be either a psycopg2 connection object or a connection string
        """
        try:
            # Se for uma string de conexão, estabelecer conexão
            if isinstance(connection, str):
                self.db_connection = psycopg2.connect(connection)
            else:
                # Se for um objeto de conexão, usar diretamente
                self.db_connection = connection
                
            # Criar tabela de logs se não existir
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
            
            # Obter schema das configurações ou usar o nome do projeto
            schema = self.project_name
            
            # Create schema if it doesn't exist
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            self.db_connection.commit()
            
            # Create logs table with the new source_file column
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.logs (
                id SERIAL PRIMARY KEY,
                task_name VARCHAR(255),
                function_name VARCHAR(255),
                source_file VARCHAR(255),
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
        """Log a new entry to both file and database with precise alignment"""
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
        
        # Quebra a mensagem em múltiplas linhas se necessário
        message_lines = textwrap.wrap(log_message, width=self.message_width)
        if not message_lines:
            message_lines = [""]
            
        # Prepara valores para cada coluna (truncando se necessário)
        values = {
            'timestamp': timestamp[:self.col_widths['timestamp']],
            'task': task_name[:self.col_widths['task']],
            'function': function_name[:self.col_widths['function']],
            'file': source_file[:self.col_widths['file']],
            'message': message_lines[0],
            'process_type': process_type.value[:self.col_widths['process_type']],
            'status': status_str[:self.col_widths['status']]
        }
        
        # Formata a linha usando o mesmo padrão de padding que o cabeçalho
        log_line = "|"
        for name, width in self.col_widths.items():
            content = values[name]
            padding_right = width - len(content) + self.padding
            log_line += " " * self.padding + content + " " * padding_right + "|"
            
        # Escreve no arquivo de log com codificação UTF-8
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line + "\n")
            
            # Se houver mais linhas na mensagem, adiciona-as com alinhamento preciso
            if len(message_lines) > 1:
                # Cria linha de continuação para cada linha adicional da mensagem
                for i in range(1, len(message_lines)):
                    cont_line = "|"
                    for name, width in self.col_widths.items():
                        if name == 'message':
                            # A coluna de mensagem tem conteúdo
                            content = message_lines[i]
                            padding_right = width - len(content) + self.padding
                            cont_line += " " * self.padding + content + " " * padding_right + "|"
                        else:
                            # Outras colunas ficam vazias
                            cont_line += " " * (width + self.padding * 2) + "|"
                    f.write(cont_line + "\n")
            
            # Adiciona separador após erros críticos para ênfase
            if status == LogStatus.CRITICAL:
                f.write(self._create_separator_line() + "\n")
        
        # Log to console
        log_level = self._get_log_level(status)
        logging.log(log_level, f"{task_name} - {function_name}: {log_message}")
        
        # Save to database if connected
        self._log_to_database(task_name, function_name, source_file, cpu_usage, memory_usage, 
                             log_date, log_time, log_message, process_type, status, extra_data)
    
    def _add_closing_line(self):
        """Add closing line to log file on program exit with exact alignment"""
        if hasattr(self, 'log_file') and self.log_file and os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(self._create_separator_line() + "\n")
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
            return False
            
        try:
            cursor = self.db_connection.cursor()
            
            # Converter process_type e status para string se forem enum
            process_type_value = process_type.value if hasattr(process_type, 'value') else str(process_type)
            status_value = status.value if hasattr(status, 'value') else str(status)
            
            sql = f"""
            INSERT INTO {self.project_name}.logs 
            (task_name, function_name, source_file, cpu_usage, memory_usage, log_date, log_time, 
            log_message, process_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(
                sql,
                (task_name, function_name, source_file, cpu_usage, memory_usage, log_date, log_time, 
                log_message, process_type_value, status_value)
            )
            
            self.db_connection.commit()
            cursor.close()
            return True
        except Exception as e:
            logging.error(f"Failed to log to database: {e}")
            return False
    
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