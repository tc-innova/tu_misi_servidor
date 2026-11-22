from functools import wraps
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def registrar_auditoria(
    db: AsyncSession,
    id_tenant: int,
    id_usuario: int,
    tabla: str,
    id_registro: str,
    accion: str,
    datos_anteriores: dict = None,
    datos_nuevos: dict = None
):
    ahora = datetime.now()
    query = text("""
        INSERT INTO auditorias (
            id_tenant, id_usuario, tabla, id_registro, accion,
            datos_anteriores, datos_nuevos, fecha, hora
        ) VALUES (
            :id_tenant, :id_usuario, :tabla, :id_registro, :accion,
            :datos_anteriores::jsonb, :datos_nuevos::jsonb, :fecha, :hora
        )
    """)
    
    await db.execute(query, {
        "id_tenant": id_tenant,
        "id_usuario": id_usuario,
        "tabla": tabla,
        "id_registro": str(id_registro),
        "accion": accion,
        "datos_anteriores": datos_anteriores,
        "datos_nuevos": datos_nuevos,
        "fecha": ahora.date(),
        "hora": ahora.time()
    })

def auditar(tabla: str, accion: str):
    def decorador(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            resultado = await func(self, *args, **kwargs)
            
            if hasattr(self, 'db') and resultado:
                id_tenant = None
                id_usuario = None
                id_registro = None
                datos_nuevos = None
                
                if isinstance(resultado, dict):
                    id_tenant = resultado.get('id_tenant')
                    id_registro = resultado.get(f'id_{tabla.rstrip("s")}')
                    datos_nuevos = dict(resultado)
                
                if id_tenant and id_registro:
                    await registrar_auditoria(
                        self.db,
                        id_tenant,
                        id_usuario,
                        tabla,
                        id_registro,
                        accion,
                        datos_nuevos=datos_nuevos
                    )
            
            return resultado
        return wrapper
    return decorador
