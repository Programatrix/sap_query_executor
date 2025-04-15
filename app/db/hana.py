# app/db/hana.py
from hdbcli import dbapi
from app.models import ConnectionInfo

def execute_hana(query: str, conn_info: ConnectionInfo):
    conn = dbapi.connect(
        address=conn_info.host,
        port=conn_info.port or 30015,
        user=conn_info.user,
        password=conn_info.password,
        databaseName=conn_info.database  # solo si es necesario
    )
    cursor = conn.cursor()
    cursor.execute(f'SET SCHEMA "{conn_info.schema}"')
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

