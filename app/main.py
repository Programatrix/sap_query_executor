from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Literal, Optional, List
from app.db.sql import execute_sql_server
from app.db.hana import execute_hana
from app.validator import is_query_safe
from app.db.storage import load_connection_for_user, save_connection_for_user, list_connections_for_user, delete_connection_for_user
from app.models import ConnectionInfo, QueryRequest, ConnectionCreateRequest
app = FastAPI()


# ------------------------
# Endpoint principal
# ------------------------
@app.post("/execute_query")
def execute_query(request: QueryRequest, x_user_id: str = Header(...)):
    if not is_query_safe(request.query):
        raise HTTPException(
            status_code=400,
            detail="Query not allowed. Must be a single SELECT and safe."
        )

    try:
        config_dict = load_connection_for_user(x_user_id, request.connection_id)
        conn_obj = ConnectionInfo(**config_dict)

        if request.engine == "sql":
            rows = execute_sql_server(request.query, conn_obj)
        elif request.engine == "hana":
            rows = execute_hana(request.query, conn_obj)
        else:
            raise HTTPException(status_code=400, detail="Invalid engine type")

        return {
            "status": "ok",
            "engine": request.engine,
            "rows": rows
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
# ------------------------
# Endpoint: Crear nueva conexión para un usuario
# ------------------------
@app.post("/connections")
def create_connection(request: ConnectionCreateRequest, x_user_id: str = Header(...)):
    try:
        save_connection_for_user(x_user_id, request.connection_id, request.dict(exclude={"connection_id"}))
        return {"status": "ok", "message": f"Connection '{request.connection_id}' saved for user '{x_user_id}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------
# ✅ NUEVO: Obtener detalles de una conexión específica
# ------------------------
@app.get("/connections/{connection_id}", response_model=ConnectionInfo)
def get_connection(connection_id: str, x_user_id: str = Header(...)):
    try:
        config = load_connection_for_user(x_user_id, connection_id)
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ------------------------
# Endpoint: Listar conexiones disponibles para el usuario
# ------------------------
@app.get("/connections", response_model=List[str])
def get_connections(x_user_id: str = Header(...)):
    return list_connections_for_user(x_user_id)

# ------------------------
# Endpoint: Actualizar conexión existente
# ------------------------
@app.put("/connections/{connection_id}")
def update_connection(connection_id: str, request: ConnectionInfo, x_user_id: str = Header(...)):
    try:
        save_connection_for_user(x_user_id, connection_id, request.dict())
        return {
            "status": "ok",
            "message": f"Connection '{connection_id}' updated for user '{x_user_id}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------
# Endpoint: Eliminar una conexión del usuario
# ------------------------
@app.delete("/connections/{connection_id}")
def delete_connection(connection_id: str, x_user_id: str = Header(...)):
    try:
        delete_connection_for_user(x_user_id, connection_id)
        return {
            "status": "ok",
            "message": f"Connection '{connection_id}' deleted for user '{x_user_id}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))