from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic.main import BaseModel


class Priority(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Event(BaseModel):
    id: int
    is_promo: bool
    priority: Priority
    template_id: int
    user_ids: Optional[List[str]]
    user_categories: Optional[List[str]]
    context: Dict[str, Any]

    class Config:
        use_enum_values = True
