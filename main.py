from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import router as api_router
from app.nucleo.configuracion import configuracion
from app.nucleo.base_datos import motor, obtener_db
from app.nucleo.limitador import limiter, manejador_exceso_limite

@asynccontextmanager
async def vida_util(app: FastAPI):
    yield
    await motor.dispose()

app = FastAPI(
    title="Tu Misi API",
    description="API para sistema de gestión de ventas e inventario",
    version="1.0.0",
    lifespan=vida_util,
    debug=configuracion.es_desarrollo,
    docs_url="/docs" if configuracion.es_desarrollo else None,
    redoc_url="/redoc" if configuracion.es_desarrollo else None,
    openapi_url="/openapi.json" if configuracion.es_desarrollo else None
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, manejador_exceso_limite)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.cors_origins_list,
    allow_credentials=configuracion.cors_allow_credentials,
    allow_methods=configuracion.cors_allow_methods.split(",") if configuracion.cors_allow_methods != "*" else ["*"],
    allow_headers=configuracion.cors_allow_headers.split(",") if configuracion.cors_allow_headers != "*" else ["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
@limiter.limit("10/minute")
async def raiz(request: Request):
    return {"mensaje": "Tu Misi API está funcionando", "entorno": configuracion.entorno}

@app.get("/salud")
@limiter.limit("30/minute")
async def verificar_salud(request: Request):
    estado = {"api": "funcionando", "entorno": configuracion.entorno}
    
    try:
        async for db in obtener_db():
            await db.execute(text("SELECT 1"))
            estado["base_datos"] = "conectada"
            break
    except Exception as e:
        estado["base_datos"] = "error"
        estado["error"] = str(e)
    
    return estado
