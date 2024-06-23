import sqlalchemy as sa

from models.db_models.base_engine import Model, RecordTimestampFields
from models.db_models.currency import Currency

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


class Rate(Model, RecordTimestampFields):
    __tablename__ = "rate"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    currency_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Currency.id, ondelete="CASCADE"),
        nullable=False,
    )
    scale = sa.Column(sa.Integer, nullable=False)
    official_rate = sa.Column(sa.DECIMAL(precision=10, scale=2, asdecimal=True))
    on_date = sa.Column(sa.Date)
