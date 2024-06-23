import sqlalchemy as sa
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from db import ro_session_dep

root_router = APIRouter()


@root_router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck(db=ro_session_dep):
    try:
        result = await db.execute(sa.text("SELECT 1"))
        if result:
            status_code = status.HTTP_200_OK
            text = "ok"
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            text = "error"
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        text = str(e)

    return JSONResponse({"status": text}, status_code)
