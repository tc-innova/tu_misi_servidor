from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.manejadores import manejar_integridad
from app.nucleo.auditoria import auditar

class ServicioCliente:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Cliente", "CI o NIT")
    @auditar("clientes", "crear")
    async def crear(self, cliente):
        query_cliente = text("""
            INSERT INTO clientes (id_tenant, nombres, apellido_paterno, apellido_materno, ci, nit, activo)
            VALUES (:id_tenant, :nombres, :apellido_paterno, :apellido_materno, :ci, :nit, :activo)
            RETURNING id_cliente
        """)
        
        resultado = await self.db.execute(query_cliente, {
            "id_tenant": cliente.id_tenant,
            "nombres": cliente.nombres,
            "apellido_paterno": cliente.apellido_paterno,
            "apellido_materno": cliente.apellido_materno,
            "ci": cliente.ci,
            "nit": cliente.nit,
            "activo": cliente.activo
        })
        id_cliente = resultado.scalar()
        await self.db.commit()
        return await self.obtener_por_id(id_cliente)
    
    @manejar_integridad("Celular", "número")
    @auditar("celulares_clientes", "crear")
    async def agregar_celular(self, id_cliente: int, celular):
        query_verificar = text("SELECT 1 FROM clientes WHERE id_cliente = :id_cliente")
        resultado = await self.db.execute(query_verificar, {"id_cliente": id_cliente})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Cliente")
        
        query = text("""
            INSERT INTO celulares_clientes (id_cliente, codigo_pais, numero)
            VALUES (:id_cliente, :codigo_pais, :numero)
            RETURNING id_celular, id_cliente, codigo_pais, numero
        """)
        resultado = await self.db.execute(query, {
            "id_cliente": id_cliente,
            "codigo_pais": celular.codigo_pais,
            "numero": celular.numero
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    @manejar_integridad("Correo", "correo")
    @auditar("correos_clientes", "crear")
    async def agregar_correo(self, id_cliente: int, correo):
        query_verificar = text("SELECT 1 FROM clientes WHERE id_cliente = :id_cliente")
        resultado = await self.db.execute(query_verificar, {"id_cliente": id_cliente})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Cliente")
        
        query = text("""
            INSERT INTO correos_clientes (id_cliente, correo)
            VALUES (:id_cliente, :correo)
            RETURNING id_correo, id_cliente, correo
        """)
        resultado = await self.db.execute(query, {
            "id_cliente": id_cliente,
            "correo": correo.correo
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def eliminar_celular(self, id_celular: int):
        query = text("DELETE FROM celulares_clientes WHERE id_celular = :id_celular RETURNING id_celular")
        resultado = await self.db.execute(query, {"id_celular": id_celular})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Celular")
        await self.db.commit()
    
    async def eliminar_correo(self, id_correo: int):
        query = text("DELETE FROM correos_clientes WHERE id_correo = :id_correo RETURNING id_correo")
        resultado = await self.db.execute(query, {"id_correo": id_correo})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Correo")
        await self.db.commit()
    
    async def listar_celulares(self, id_cliente: int):
        query = text("""
            SELECT id_celular, id_cliente, codigo_pais, numero
            FROM celulares_clientes
            WHERE id_cliente = :id_cliente
        """)
        resultado = await self.db.execute(query, {"id_cliente": id_cliente})
        return resultado.mappings().all()
    
    async def listar_correos(self, id_cliente: int):
        query = text("""
            SELECT id_correo, id_cliente, correo
            FROM correos_clientes
            WHERE id_cliente = :id_cliente
        """)
        resultado = await self.db.execute(query, {"id_cliente": id_cliente})
        return resultado.mappings().all()
    
    async def obtener_por_id(self, id_cliente: int):
        query = text("""
            SELECT id_cliente, id_tenant, nombres, apellido_paterno, apellido_materno, ci, nit, activo
            FROM clientes
            WHERE id_cliente = :id_cliente
        """)
        resultado = await self.db.execute(query, {"id_cliente": id_cliente})
        cliente = resultado.mappings().first()
        if not cliente:
            raise ExcepcionNoEncontrado("Cliente")
        return cliente
    
    async def listar_por_tenant(self, id_tenant: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_cliente, id_tenant, nombres, apellido_paterno, apellido_materno, ci, nit, activo
            FROM clientes
            WHERE id_tenant = :id_tenant
            ORDER BY id_cliente
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": id_tenant,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
