from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.manejadores import manejar_integridad
from app.nucleo.auditoria import auditar

class ServicioTenant:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Tenant", "nombre")
    @auditar("tenants", "crear")
    async def crear(self, tenant):
        query = text("""
            INSERT INTO tenants (nombre)
            VALUES (:nombre)
            RETURNING id_tenant, nombre
        """)
        resultado = await self.db.execute(query, {"nombre": tenant.nombre})
        await self.db.commit()
        return resultado.mappings().first()
    
    async def obtener_por_id(self, id_tenant: int):
        query = text("""
            SELECT id_tenant, nombre
            FROM tenants
            WHERE id_tenant = :id_tenant
        """)
        resultado = await self.db.execute(query, {"id_tenant": id_tenant})
        tenant = resultado.mappings().first()
        if not tenant:
            raise ExcepcionNoEncontrado("Tenant")
        return tenant
    
    async def listar(self, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_tenant, nombre
            FROM tenants
            ORDER BY id_tenant
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {"skip": skip, "limit": limit})
        return resultado.mappings().all()
