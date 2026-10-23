
from django.db import connection

def testar_conexao_supabase():
    """Executa uma consulta simples para homologar a conexao com o Supabase."""
    query = "SELECT NOW() AS hora_servidor, current_database() AS nome_banco, version() AS versao_postgres;"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultado = cursor.fetchone()
        
    print("=== CONEXÃO COM POSTGRESQL NO SUPABASE ===")
    print(f"Data/Hora no Servidor: {resultado[0]}")
    print(f"Banco Conectado:       {resultado[1]}")
    print(f"Versão do PostgreSQL:  {resultado[2]}")

if __name__ == "__main__":
    testar_conexao_supabase()