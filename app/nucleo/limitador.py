from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

async def manejador_exceso_limite(request: Request, exc: RateLimitExceeded) -> Response:
    return JSONResponse(
        status_code=429,
        content={"detalle": "Demasiadas peticiones. Intenta más tarde."}
    )
