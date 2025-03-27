
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"message": e.detail}
            )
        except Exception as e:
            logging.exception("Unhandled error")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Erro interno do servidor"}
            )
