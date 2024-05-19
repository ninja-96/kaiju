from pydantic import BaseModel


__all__ = [
    'BaseItem'
]


class BaseItem(BaseModel):
    class Config:
        arbitrary_types_allowed = True
