#!/usr/bin/env python3
import asyncio

import asyncpg
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings as s
from db import db_url
from models import db_models as m
from tests.conftest import check_test_db

psql_url = f"postgresql+asyncpg://{s.DATABASE_USER}:{s.DATABASE_PASSWORD}@{s.DATABASE_HOST}:5432"


async def setup_db_for_tests():
    check_test_db()
    conn = await asyncpg.connect(psql_url.replace("+asyncpg", ""))
    # Execute a statement to create a new table.
    await conn.execute("commit")
    await conn.execute(f"drop database if exists {s.DATABASE_DB}")
    await conn.execute("commit")
    await conn.execute(f"create database {s.DATABASE_DB}")
    await conn.execute("commit")
    await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    await conn.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
    await conn.execute("commit")
    await conn.close()

    e = create_async_engine(db_url)
    async with e.begin() as conn:
        await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS unaccent"))
        await conn.execute(sa.text("commit"))
        await conn.run_sync(m.Model.metadata.create_all)
        await conn.execute(sa.text("commit"))
    await e.dispose()


if __name__ == "__main__":
    asyncio.run(setup_db_for_tests())
