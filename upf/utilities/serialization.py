from typing import Any

def serialize_payload(payload: Any) -> Any:
    """
    Converts Pydantic models into JSON-serializable dicts.
    Leaves dicts / primitives untouched.
    """

    if hasattr(payload, "model_dump"):
        return payload.model_dump(mode="json")
    
    return payload