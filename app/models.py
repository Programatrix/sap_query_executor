from pydantic import BaseModel
from typing import Literal, Optional

class ConnectionInfo(BaseModel):
    host: str
    port: Optional[int] = None
    user: str
    password: str
    schema: Optional[str] = None
    database: Optional[str] = None

class ConnectionCreateRequest(ConnectionInfo):
    connection_id: str

class QueryRequest(BaseModel):
    engine: Literal["sql", "hana"]
    query: str
    connection: ConnectionInfo
