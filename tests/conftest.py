import asyncio
import base64

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from api_main import app
from config import settings as st
from db import get_session_dep
from models.db_models import Model
from utils.request_logging_middleware import RequestsLoggingMiddleware
from .creator import Creator

import sqlalchemy as sa
from models import db_models as m

db_url = (
    "postgresql+asyncpg://"
    f"{st.DATABASE_USER}:"
    f"{st.DATABASE_PASSWORD}@"
    f"{st.DATABASE_HOST}:"
    f"{st.DATABASE_PORT}/"
    f"{st.DATABASE_DB}"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def check_test_db():
    if st.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres"):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture(scope="session")
async def engine():
    check_test_db()

    e = create_async_engine(db_url, echo=False, max_overflow=25)
    try:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.create_all)

        yield e
    finally:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.drop_all)


@pytest.fixture
async def dbsession(engine) -> AsyncSession:
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest.fixture
async def test_client_rest(dbsession: AsyncSession) -> AsyncClient:
    def override_get_db():
        test_db = dbsession
        yield test_db

    async def _override_save_request_log(data, *args, **kwargs):
        await dbsession.execute(sa.insert(m.RequestLog).values(data))

    app.dependency_overrides[get_session_dep.dependency] = override_get_db

    for middleware in app.user_middleware:
        # generally this function creates own session since we cannot access the session on middleware level
        # so we override this function to one which does not create new session but uses the one from the fixture instead
        if isinstance(middleware, RequestsLoggingMiddleware):
            middleware._save_request_log = _override_save_request_log

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def creator(dbsession) -> Creator:
    return Creator(dbsession)


@pytest.fixture
def auth_token() -> str:
    return (
        "Basic "
        + base64.b64encode(f"{st.WEB_LOGIN}:{st.WEB_PASSWORD}".encode()).decode()
    )
