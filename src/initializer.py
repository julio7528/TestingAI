# Módulo principal para inicialização da aplicação
# Este arquivo pode ser importado de qualquer lugar para garantir que a aplicação seja inicializada

from src.utils.app_initializer import initialize_app

# Inicializa a aplicação quando o módulo é importado
logger, db_manager = initialize_app()

# Exporta variáveis importantes
__all__ = ['logger', 'db_manager']