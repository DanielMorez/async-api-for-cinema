from typing import Any, Dict, List, Optional

from pydantic.main import BaseModel


class Event(BaseModel):
    is_promo: bool
    template_id: int
    user_ids: Optional[List[str]]
    context: Dict[str, Any]

    class Config:
        use_enum_values = True


class Template(BaseModel):
    title: str
    code: str
    template: str
    subject: str
