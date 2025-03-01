# Carrega ambiente primeiro, antes de qualquer outra coisa
from src.utils.environment_loader import environment

# Agora pode importar outros módulos que dependem das configurações
from src.utils.app_initializer import initialize_app

# Inicializa a aplicação quando o módulo é importado
logger, db_manager = initialize_app()

# Exporta variáveis importantes
__all__ = ['logger', 'db_manager', 'environment']