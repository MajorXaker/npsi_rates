import sqlalchemy as sa

from models.db_models.base_engine import Model, RecordTimestampFields


class Config(Model, RecordTimestampFields):
    __tablename__ = "config"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
