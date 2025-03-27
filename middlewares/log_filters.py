import logging
import contextvars

request_id_var = contextvars.ContextVar("request_id", default="N/A")

class RequestIdFilter(logging.Filter):
    """
    Filtro que adiciona automaticamente request_id a todos os logs.
    """
    def filter(self, record):
        record.request_id = request_id_var.get()  
        return True
