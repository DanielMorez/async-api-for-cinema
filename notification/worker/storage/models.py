from pydantic import BaseModel


class Template(BaseModel):
    id: int
    title: str
    subject: str
    content: str
    type: str
