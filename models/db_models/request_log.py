import sqlalchemy as sa

from models.db_models.base_engine import Model


class RequestLog(Model):
    __tablename__ = "request_logs"

    id = sa.Column(sa.Integer, primary_key=True)
    endpoint_address = sa.Column(sa.String)
    method = sa.Column(sa.String(10))
    datetime = sa.Column(sa.DateTime)
    requester_ip = sa.Column(sa.String(25))
    user_agent = sa.Column(sa.Text)
    request_data = sa.Column(sa.JSON)
    response_code = sa.Column(sa.Integer)
