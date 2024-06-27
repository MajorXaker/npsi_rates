from datetime import datetime
from functools import wraps

import sqlalchemy as sa
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from db import persistent_engine
from models import db_models as m


class RequestsLoggingMiddleware(BaseHTTPMiddleware):

    async def _save_request_log(self, data: dict):
        async with AsyncSession(persistent_engine) as session, session.begin():
            await session.execute(sa.insert(m.RequestLog).values(data))

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logged_data = {
            m.RequestLog.datetime: datetime.utcnow(),
            m.RequestLog.requester_ip: request.client.host,
            m.RequestLog.user_agent: request.headers.get("User-Agent"),
            m.RequestLog.endpoint_address: request.url.path,
            m.RequestLog.method: request.method,
            m.RequestLog.request_data: dict(request.query_params),
            m.RequestLog.response_code: response.status_code,
        }
        await self._save_request_log(logged_data)
        return response


class RequestsIntercepror:
    def __init__(self): ...

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)

            request_data = kwargs["request"]
            print("TRIGGERED")

            log_data = {
                m.RequestLog.datetime: datetime.utcnow(),
                m.RequestLog.requester_ip: request_data.client.host,
                m.RequestLog.user_agent: request_data.headers.get("User-Agent"),
                m.RequestLog.endpoint_address: request_data.url.path,
                m.RequestLog.response_data: response.json(),
                m.RequestLog.request_data: dict(request_data.query_params),
            }

            await kwargs["db"].execute(sa.insert(m.RequestLog).values(log_data))

            return response

        return wrapper


requests_interceptor = RequestsIntercepror()
