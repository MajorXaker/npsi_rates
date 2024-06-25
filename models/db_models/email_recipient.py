import sqlalchemy as sa

from models.db_models.base_engine import Model, RecordTimestampFields


class EmailRecipient(Model, RecordTimestampFields):
    __tablename__ = "email_recipients"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.Text, nullable=False, unique=True)
