import json
import os
from fastapi import HTTPException

CONNECTIONS_DIR = "connections"

os.makedirs(CONNECTIONS_DIR, exist_ok=True)

def _get_user_file(user_id: str) -> str:
    return os.path.join(CONNECTIONS_DIR, f"{user_id}.json")

def load_connection_for_user(user_id: str, connection_id: str) -> dict:
    user_file = _get_user_file(user_id)
    if not os.path.exists(user_file):
        raise HTTPException(status_code=404, detail="No connections found for user")

    with open(user_file, "r") as f:
        connections = json.load(f)

    if connection_id not in connections:
        raise HTTPException(status_code=404, detail="Connection ID not found for this user")

    return connections[connection_id]

def save_connection_for_user(user_id: str, connection_id: str, config: dict):
    user_file = _get_user_file(user_id)
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            connections = json.load(f)
    else:
        connections = {}

    connections[connection_id] = config

    with open(user_file, "w") as f:
        json.dump(connections, f, indent=2)

def list_connections_for_user(user_id: str) -> list:
    user_file = _get_user_file(user_id)
    if not os.path.exists(user_file):
        return []

    with open(user_file, "r") as f:
        connections = json.load(f)
    return list(connections.keys())

def delete_connection_for_user(user_id: str, connection_id: str):
    user_file = _get_user_file(user_id)
    if not os.path.exists(user_file):
        raise HTTPException(status_code=404, detail="No connections found for user")
    with open(user_file, "r") as f:
        connections = json.load(f)

    if connection_id not in connections:
        raise HTTPException(status_code=404, detail="Connection ID not found")

    del connections[connection_id]

    with open(user_file, "w") as f:
        json.dump(connections, f, indent=2)
