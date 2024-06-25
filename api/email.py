from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
import models.db_models as m
from db import get_session_dep
from models.api_models.email import (
    EmailCreatedResponse,
    EmailDeletedResponse,
    EmailsResponse,
)

email_router = APIRouter()


@email_router.post("/email_recipients", tags=["email_recipients"])
async def add_email_recipient(
    email: str,
    db: AsyncSession = get_session_dep,
) -> EmailCreatedResponse:
    try:
        email_id = await db.scalar(
            sa.insert(m.EmailRecipient)
            .values(email=email)
            .returning(m.EmailRecipient.id)
        )
        return EmailCreatedResponse(id=email_id, email=email, status="Created")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))


@email_router.delete("/email_recipients", tags=["email_recipients"])
async def delete_email_recipient(
    email: str,
    db: AsyncSession = get_session_dep,
) -> EmailDeletedResponse:
    try:
        await db.execute(
            sa.delete(m.EmailRecipient).where(m.EmailRecipient.email == email)
        )
        return EmailDeletedResponse(status=f"Deleted {email}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))


@email_router.get("/email_recipients", tags=["email_recipients"])
async def get_email_recipients(
    db: AsyncSession = get_session_dep,
) -> EmailsResponse:
    emails = (
        (
            await db.scalars(
                sa.select(m.EmailRecipient.email).select_from(m.EmailRecipient)
            )
        )
    ).fetchall()
    return EmailsResponse(emails=emails)
