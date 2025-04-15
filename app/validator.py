import re

def is_query_safe(query: str) -> bool:
    lowered = query.lower().strip()
    forbidden = [
        "update", "delete", "insert", "drop",
        "alter", "exec", "merge", "truncate"
    ]
    if not lowered.startswith("select"):
        return False
    if any(kw in lowered for kw in forbidden):
        return False
    if ";" in lowered:
        return False
    return True
