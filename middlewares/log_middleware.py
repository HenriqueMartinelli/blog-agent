# middleware/log_middleware.py

import uuid
import logging
from fastapi import Request
from middlewares.log_filters import request_id_var 

logger = logging.getLogger("root")

class LogMiddleware:
    async def __call__(self, request: Request, call_next):
        """
        Middleware que gera um request_id único e o armazena para toda a requisição.
        """
        request_id = str(uuid.uuid4())  
        request_id_var.set(request_id)  
        logger.info(f"📌 [{request_id}] new request: {request.method} {request.url}")

        response = await call_next(request)

        logger.info(f"📌 [{request_id}] response: {response.status_code} to {request.url}")
        response.headers["X-Request-ID"] = request_id 

        return response
