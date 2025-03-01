# Esse arquivo torna o diretório src um pacote Python
# Adicionar este código permite importações mais limpas

# Permitir importação direta dos módulos principais
from src.config.settings import Settings
from src.modules.workflow import Workflow
from src.utils.logger import EnhancedLogger, ProcessType, LogStatus

# Inicializar configurações globais (opcional)
settings = Settings()