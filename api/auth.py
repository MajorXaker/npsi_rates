import secrets

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from config import settings

security = HTTPBasic()


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.WEB_LOGIN)
    correct_password = secrets.compare_digest(
        credentials.password, settings.WEB_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials
