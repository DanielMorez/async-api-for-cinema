from typing import Dict, List, Optional, Any

from pydantic import BaseModel


class Event(BaseModel):
    is_promo: bool
    template_id: int
    user_ids: Optional[List[str]]
    context: Dict[str, Any]

    class Config:
        use_enum_values = True
