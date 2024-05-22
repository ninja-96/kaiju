from pydantic import BaseModel, ConfigDict


__all__ = [
    'BaseItem'
]


class BaseItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
