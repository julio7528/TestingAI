# tests/test_db_connection.py
# Teste para verificar a conexão com o Supabase

import os
import sys
import logging

# Configura logging básico para diagnóstico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def test_db_connection():
    """Testa a conexão com o banco de dados Supabase"""
    
    logging.info("=== TESTE DE CONEXÃO COM SUPABASE ===")
    
    # 1. Verifica se conseguimos importar os módulos necessários
    try:
        import psycopg2
        logging.info("✓ Módulo psycopg2 importado com sucesso")
    except ImportError as e:
        logging.error(f"✗ Erro ao importar psycopg2: {e}")
        logging.error("Instale com: pip install psycopg2-binary")
        return False
    
    # 2. Verifica se o arquivo .env existe
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_file):
        logging.info(f"✓ Arquivo .env encontrado: {env_file}")
    else:
        logging.error(f"✗ Arquivo .env não encontrado em: {env_file}")
        logging.error(f"  Verifique se você criou o arquivo .env a partir do .env.development")
        return False
    
    # 3. Carrega as variáveis de ambiente
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        logging.info("✓ Variáveis de ambiente carregadas do arquivo .env")
    except Exception as e:
        logging.error(f"✗ Erro ao carregar variáveis de ambiente: {e}")
        return False
    
    # 4. Verifica as variáveis do banco de dados
    db_vars = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD')
    }
    
    # Verifica se todas as variáveis estão definidas
    missing_vars = [var for var, value in db_vars.items() if not value]
    if missing_vars:
        logging.error(f"✗ Variáveis de ambiente não definidas: {', '.join(missing_vars)}")
        return False
    
    logging.info("✓ Todas as variáveis de banco de dados estão definidas")
    
    # Mostra as variáveis (ocultando a senha)
    for var, value in db_vars.items():
        if var == 'DB_PASSWORD':
            display_value = '********'
        else:
            display_value = value
        logging.info(f"  {var}: {display_value}")
    
    # 5. Tenta conectar diretamente ao banco
    try:
        logging.info("Tentando conectar ao Supabase...")
        
        # Estabelece conexão direta usando as variáveis de ambiente
        conn = psycopg2.connect(
            host=db_vars['DB_HOST'],
            port=db_vars['DB_PORT'],
            database=db_vars['DB_NAME'],
            user=db_vars['DB_USER'],
            password=db_vars['DB_PASSWORD']
        )
        
        # Testa a conexão
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        cursor.close()
        
        logging.info(f"✓ Conectado com sucesso ao Supabase!")
        logging.info(f"  Versão: {version}")
        
        # Testa a criação do schema
        schema_name = 'rpa_automation'
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        conn.commit()
        cursor.close()
        
        logging.info(f"✓ Schema '{schema_name}' verificado/criado com sucesso")
        
        # Testa a criação de uma tabela temporária
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.connection_test (
            id SERIAL PRIMARY KEY,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            test_result TEXT
        )
        """)
        conn.commit()
        
        # Insere um registro de teste
        cursor.execute(f"""
        INSERT INTO {schema_name}.connection_test (test_result)
        VALUES ('Teste de conexão bem-sucedido')
        RETURNING id
        """)
        
        row_id = cursor.fetchone()[0]
        conn.commit()
        
        logging.info(f"✓ Inserção na tabela de teste bem-sucedida (ID: {row_id})")
        
        # Limpa a tabela de teste
        cursor.execute(f"DELETE FROM {schema_name}.connection_test")
        conn.commit()
        cursor.close()
        
        # Fecha a conexão
        conn.close()
        logging.info("✓ Conexão fechada com sucesso")
        
        return True
        
    except Exception as e:
        logging.error(f"✗ Erro ao conectar ao Supabase: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    if success:
        logging.info("\n=== TESTE CONCLUÍDO COM SUCESSO ===")
        sys.exit(0)
    else:
        logging.error("\n=== TESTE FALHOU ===")
        sys.exit(1)