import pyodbc

SQL_CONFIG = {
    "host": "localhost",
    "port": 1433,
    "user": "readonly",
    "password": "secret",
    "database": "SBODEMOUS"
}

def execute_sql_server(query: str):
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_CONFIG['host']};"
        f"DATABASE={SQL_CONFIG['database']};"
        f"UID={SQL_CONFIG['user']};PWD={SQL_CONFIG['password']}"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results
