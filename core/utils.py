# core/utils.py
from django.db import connection

def dictfetchall(cursor):
    """Converte todas as linhas de um cursor em uma lista de dicionarios."""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def buscar_status_nichos_banco():
    """Consulta a View SQL vw_status_nichos hospedada no Supabase."""
    query = "SELECT * FROM vw_status_nichos ORDER BY id_nicho ASC;"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = dictfetchall(cursor)
        
    return dados