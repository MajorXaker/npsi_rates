from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

"""{
    "Cur_ID": 510,
    "Date": "2023-01-10T00:00:00",
    "Cur_Abbreviation": "AMD",
    "Cur_Scale": 1000,
    "Cur_Name": "Армянских драмов",
    "Cur_OfficialRate": 6.848
  },"""


class Rate(BaseModel):
    cur_id: int = Field(serialization_alias="Cur_ID")
    date: datetime = Field(serialization_alias="Date")
    cur_abbreviation: str = Field(serialization_alias="Cur_Abbreviation")
    cur_scale: int = Field(serialization_alias="Cur_Scale")
    cur_name: str = Field(serialization_alias="Cur_Name")
    cur_official_rate: Decimal = Field(serialization_alias="Cur_OfficialRate")

    @classmethod
    def from_db_model(
        cls,
        external_id: int,
        on_date: date,
        abbreviation: str,
        scale: float,
        name: str,
        official_rate: float,
        **kwargs,
    ):
        return cls(
            cur_id=external_id,
            date=on_date,
            cur_abbreviation=abbreviation,
            cur_scale=scale,
            cur_name=name,
            cur_official_rate=official_rate,
        )
