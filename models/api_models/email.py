from pydantic import BaseModel


class EmailCreatedResponse(BaseModel):
    status: str
    id: int
    email: str


class EmailDeletedResponse(BaseModel):
    status: str


class EmailsResponse(BaseModel):
    emails: list[str]
