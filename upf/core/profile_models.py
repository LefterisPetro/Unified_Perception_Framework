from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ComponentConfig(BaseModel):
    type:str
    params: Dict[str, Any] = Field(default_factory=dict)

class ProfileConfig(BaseModel):
    sources: List[ComponentConfig]
    processors: List[ComponentConfig]
    sinks: List[ComponentConfig]
    