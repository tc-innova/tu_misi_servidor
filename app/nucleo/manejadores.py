from functools import wraps
from sqlalchemy.exc import IntegrityError
from app.nucleo.excepciones import ExcepcionDuplicado

def manejar_integridad(entidad: str, campo: str):
    def decorador(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except IntegrityError:
                db = args[0].db
                await db.rollback()
                raise ExcepcionDuplicado(entidad, campo)
        return wrapper
    return decorador
