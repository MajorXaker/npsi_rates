import sqlalchemy as sa

from models.db_models.base_engine import Model, RecordTimestampFields

"""-код валюты
-дата
-аббревиатура валюты
-единица валюты
-название валюты
-курс валюты"""

"""{
    "Cur_ID": 510,
    "Date": "2023-01-10T00:00:00",
    "Cur_Abbreviation": "AMD",
    "Cur_Scale": 1000,
    "Cur_Name": "Армянских драмов",
    "Cur_OfficialRate": 6.848
  }"""


class Currency(Model, RecordTimestampFields):
    __tablename__ = "currencies"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    abbreviation = sa.Column(sa.String(5))
    name = sa.Column(sa.String(50))
    external_id = sa.Column(sa.Integer, index=True, unique=True)
