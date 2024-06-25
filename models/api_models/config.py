from datetime import time

from pydantic import BaseModel


class Config(BaseModel):
    very_important_value: str
    step: int
    data_collection_time: time

    class Config:
        from_attributes = True
