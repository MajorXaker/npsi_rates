import sqlalchemy as sa

from models.db_models.base_engine import Model, RecordTimestampFields


class Config(Model, RecordTimestampFields):
    __tablename__ = "config"

    id = sa.Column(sa.Integer, primary_key=True)
    very_important_value = sa.Column(sa.String)
    step = sa.Column(sa.Integer)
    """
    0 - awaiting data collection
    1 - data collection in progress
    2 - saving data in progress
    3 - sending email
    4 - email sent
    """

    data_collection_time = sa.Column(sa.Time)
