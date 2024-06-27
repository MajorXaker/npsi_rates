from datetime import time
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    very_important_value: Optional[str]
    step: Optional[int]
    data_collection_time: Optional[time]

    class Config:
        from_attributes = True
