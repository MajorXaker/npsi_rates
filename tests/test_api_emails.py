import pytest
import sqlalchemy as sa

from models import db_models as m


@pytest.mark.asyncio
async def test_get_emails(test_client_rest, dbsession, auth_token):
    await dbsession.execute(
        sa.insert(m.EmailRecipient).values(email="test@example.com")
    )

    response = await test_client_rest.get(
        "/email_recipients",
        headers={"Authorization": auth_token},
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data["emails"]) > 0
    assert "test@example.com" in data["emails"]


@pytest.mark.asyncio
async def test_add_email(test_client_rest, dbsession, auth_token):
    response = await test_client_rest.post(
        "/email_recipients",
        params={"email": "new@example.com"},
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200

    query_response = await dbsession.execute(
        sa.select(m.EmailRecipient).where(m.EmailRecipient.email == "new@example.com")
    )
    email_entry = query_response.scalar_one_or_none()
    assert email_entry is not None
    assert email_entry.email == "new@example.com"


@pytest.mark.asyncio
async def test_delete_email(test_client_rest, dbsession, auth_token):
    # First, insert a test email to delete
    await dbsession.execute(
        sa.insert(m.EmailRecipient).values(email="delete_me@example.com")
    )

    response = await test_client_rest.delete(
        "/email_recipients",
        params={"email": "delete_me@example.com"},
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200

    # Verify the email was deleted
    query_response = await dbsession.execute(
        sa.select(m.EmailRecipient).where(
            m.EmailRecipient.email == "delete_me@example.com"
        )
    )
    email_entry = query_response.scalar_one_or_none()
    assert email_entry is None
