from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.manejadores import manejar_integridad
from app.nucleo.auditoria import auditar

class ServicioTipoProveedor:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Tipo de proveedor", "nombre")
    @auditar("tipo_proveedores", "crear")
    async def crear(self, tipo):
        query = text("""
            INSERT INTO tipo_proveedores (id_tenant, nombre)
            VALUES (:id_tenant, :nombre)
            RETURNING id_tipo_proveedor, id_tenant, nombre
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": tipo.id_tenant,
            "nombre": tipo.nombre
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def listar_por_tenant(self, id_tenant: int):
        query = text("""
            SELECT id_tipo_proveedor, id_tenant, nombre
            FROM tipo_proveedores
            WHERE id_tenant = :id_tenant
            ORDER BY id_tipo_proveedor
        """)
        resultado = await self.db.execute(query, {"id_tenant": id_tenant})
        return resultado.mappings().all()

class ServicioProveedor:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Proveedor", "nombre")
    @auditar("proveedores", "crear")
    async def crear(self, proveedor):
        query_proveedor = text("""
            INSERT INTO proveedores (id_tenant, id_tipo_proveedor, nombre, activo)
            VALUES (:id_tenant, :id_tipo_proveedor, :nombre, :activo)
            RETURNING id_proveedor
        """)
        
        resultado = await self.db.execute(query_proveedor, {
            "id_tenant": proveedor.id_tenant,
            "id_tipo_proveedor": proveedor.id_tipo_proveedor,
            "nombre": proveedor.nombre,
            "activo": proveedor.activo
        })
        id_proveedor = resultado.scalar()
        await self.db.commit()
        return await self.obtener_por_id(id_proveedor)
    
    @manejar_integridad("Celular", "número")
    @auditar("celulares_proveedores", "crear")
    async def agregar_celular(self, id_proveedor: int, celular):
        query_verificar = text("SELECT 1 FROM proveedores WHERE id_proveedor = :id_proveedor")
        resultado = await self.db.execute(query_verificar, {"id_proveedor": id_proveedor})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Proveedor")
        
        query = text("""
            INSERT INTO celulares_proveedores (id_proveedor, codigo_pais, numero)
            VALUES (:id_proveedor, :codigo_pais, :numero)
            RETURNING id_celular, id_proveedor, codigo_pais, numero
        """)
        resultado = await self.db.execute(query, {
            "id_proveedor": id_proveedor,
            "codigo_pais": celular.codigo_pais,
            "numero": celular.numero
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    @manejar_integridad("Correo", "correo")
    @auditar("correos_proveedores", "crear")
    async def agregar_correo(self, id_proveedor: int, correo):
        query_verificar = text("SELECT 1 FROM proveedores WHERE id_proveedor = :id_proveedor")
        resultado = await self.db.execute(query_verificar, {"id_proveedor": id_proveedor})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Proveedor")
        
        query = text("""
            INSERT INTO correos_proveedores (id_proveedor, correo)
            VALUES (:id_proveedor, :correo)
            RETURNING id_correo, id_proveedor, correo
        """)
        resultado = await self.db.execute(query, {
            "id_proveedor": id_proveedor,
            "correo": correo.correo
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def eliminar_celular(self, id_celular: int):
        query = text("DELETE FROM celulares_proveedores WHERE id_celular = :id_celular RETURNING id_celular")
        resultado = await self.db.execute(query, {"id_celular": id_celular})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Celular")
        await self.db.commit()
    
    async def eliminar_correo(self, id_correo: int):
        query = text("DELETE FROM correos_proveedores WHERE id_correo = :id_correo RETURNING id_correo")
        resultado = await self.db.execute(query, {"id_correo": id_correo})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Correo")
        await self.db.commit()
    
    async def listar_celulares(self, id_proveedor: int):
        query = text("""
            SELECT id_celular, id_proveedor, codigo_pais, numero
            FROM celulares_proveedores
            WHERE id_proveedor = :id_proveedor
        """)
        resultado = await self.db.execute(query, {"id_proveedor": id_proveedor})
        return resultado.mappings().all()
    
    async def listar_correos(self, id_proveedor: int):
        query = text("""
            SELECT id_correo, id_proveedor, correo
            FROM correos_proveedores
            WHERE id_proveedor = :id_proveedor
        """)
        resultado = await self.db.execute(query, {"id_proveedor": id_proveedor})
        return resultado.mappings().all()
    
    async def obtener_por_id(self, id_proveedor: int):
        query = text("""
            SELECT id_proveedor, id_tenant, id_tipo_proveedor, nombre, activo
            FROM proveedores
            WHERE id_proveedor = :id_proveedor
        """)
        resultado = await self.db.execute(query, {"id_proveedor": id_proveedor})
        proveedor = resultado.mappings().first()
        if not proveedor:
            raise ExcepcionNoEncontrado("Proveedor")
        return proveedor
    
    async def listar_por_tenant(self, id_tenant: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_proveedor, id_tenant, id_tipo_proveedor, nombre, activo
            FROM proveedores
            WHERE id_tenant = :id_tenant
            ORDER BY id_proveedor
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": id_tenant,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
