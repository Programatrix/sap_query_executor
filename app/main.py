from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from app.db.sql import execute_sql_server
from app.db.hana import execute_hana
from app.validator import is_query_safe
from app.models import QueryRequest, ConnectionInfo


app = FastAPI()

# ------------------------
# Endpoint principal
# ------------------------
@app.post("/execute_query")
def execute_query(request: QueryRequest):
    if not is_query_safe(request.query):
        raise HTTPException(
            status_code=400,
            detail="Query not allowed. Must be a single SELECT and safe."
        )

    try:
        if request.engine == "sql":
            rows = execute_sql_server(request.query, request.connection)
        elif request.engine == "hana":
            rows = execute_hana(request.query, request.connection)
        else:
            raise HTTPException(status_code=400, detail="Invalid engine type")

        return {
            "status": "ok",
            "engine": request.engine,
            "rows": rows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
