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
    query = "SELECT * FROM vw_status_nicho ORDER BY nicho_id ASC;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = dictfetchall(cursor)

    return dados