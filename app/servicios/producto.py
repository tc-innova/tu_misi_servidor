from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.manejadores import manejar_integridad
from app.nucleo.auditoria import auditar

class ServicioTipoProducto:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Tipo de producto", "nombre")
    @auditar("tipo_productos", "crear")
    async def crear(self, tipo):
        query = text("""
            INSERT INTO tipo_productos (id_tenant, nombre)
            VALUES (:id_tenant, :nombre)
            RETURNING id_tipo_producto, id_tenant, nombre
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": tipo.id_tenant,
            "nombre": tipo.nombre
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def listar_por_tenant(self, id_tenant: int):
        query = text("""
            SELECT id_tipo_producto, id_tenant, nombre
            FROM tipo_productos
            WHERE id_tenant = :id_tenant
            ORDER BY id_tipo_producto
        """)
        resultado = await self.db.execute(query, {"id_tenant": id_tenant})
        return resultado.mappings().all()

class ServicioProducto:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Producto", "código")
    @auditar("productos", "crear")
    async def crear(self, producto):
        query = text("""
            INSERT INTO productos (id_tipo_producto, codigo, nombre, precio, cantidad, cantidad_minima, activo)
            VALUES (:id_tipo_producto, :codigo, :nombre, :precio, :cantidad, :cantidad_minima, :activo)
            RETURNING id_producto, id_tipo_producto, codigo, nombre, precio, cantidad, cantidad_minima, activo
        """)
        resultado = await self.db.execute(query, {
            "id_tipo_producto": producto.id_tipo_producto,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad,
            "cantidad_minima": producto.cantidad_minima,
            "activo": producto.activo
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def obtener_por_id(self, id_producto: int):
        query = text("""
            SELECT id_producto, id_tipo_producto, codigo, nombre, precio, cantidad, cantidad_minima, activo
            FROM productos
            WHERE id_producto = :id_producto
        """)
        resultado = await self.db.execute(query, {"id_producto": id_producto})
        producto = resultado.mappings().first()
        if not producto:
            raise ExcepcionNoEncontrado("Producto")
        return producto
    
    async def listar_por_tipo(self, id_tipo_producto: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_producto, id_tipo_producto, codigo, nombre, precio, cantidad, cantidad_minima, activo
            FROM productos
            WHERE id_tipo_producto = :id_tipo_producto
            ORDER BY id_producto
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_tipo_producto": id_tipo_producto,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
