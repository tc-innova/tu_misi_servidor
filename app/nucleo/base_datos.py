from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.nucleo.configuracion import configuracion

motor = create_async_engine(
    configuracion.database_url,
    pool_size=configuracion.db_pool_size,
    max_overflow=configuracion.db_max_overflow,
    pool_timeout=configuracion.db_pool_timeout,
    pool_recycle=configuracion.db_pool_recycle,
    echo=False
)

FabricaSesionAsync = async_sessionmaker(
    motor,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def obtener_db():
    async with FabricaSesionAsync() as sesion:
        try:
            yield sesion
        finally:
            await sesion.close()
