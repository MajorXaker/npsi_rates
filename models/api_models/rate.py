from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, AliasChoices

"""{
    "Cur_ID": 510,
    "Date": "2023-01-10T00:00:00",
    "Cur_Abbreviation": "AMD",
    "Cur_Scale": 1000,
    "Cur_Name": "Армянских драмов",
    "Cur_OfficialRate": 6.848
  },"""


class Rate(BaseModel):
    Cur_ID: int
    Date: datetime
    Cur_Abbreviation: str
    Cur_Scale: int
    Cur_Name: str
    Cur_OfficialRate: Decimal

    @classmethod
    def from_db_model(
        cls,
        database_row,
    ):
        return cls(
            Cur_ID=database_row.external_id,
            Date=database_row.on_date,
            Cur_Abbreviation=database_row.abbreviation,
            Cur_Scale=database_row.scale,
            Cur_Name=database_row.name,
            Cur_OfficialRate=database_row.official_rate,
        )


class RatesResponse(BaseModel):
    rates: list[Rate]
