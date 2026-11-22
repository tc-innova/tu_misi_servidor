from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.auditoria import auditar

class ServicioCompra:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @auditar("compras", "crear")
    async def crear(self, compra):
        query_compra = text("""
            INSERT INTO compras (id_proveedor, id_usuario, id_estado_compra, fecha_compra, hora_compra)
            VALUES (:id_proveedor, :id_usuario, :id_estado_compra, :fecha_compra, :hora_compra)
            RETURNING id_compra
        """)
        
        resultado = await self.db.execute(query_compra, {
            "id_proveedor": compra.id_proveedor,
            "id_usuario": compra.id_usuario,
            "id_estado_compra": compra.id_estado_compra,
            "fecha_compra": compra.fecha_compra,
            "hora_compra": compra.hora_compra
        })
        id_compra = resultado.scalar()
        
        for detalle in compra.detalles:
            query_verificar = text("""
                SELECT id_producto FROM productos WHERE id_producto = :id_producto
            """)
            resultado_producto = await self.db.execute(query_verificar, {"id_producto": detalle.id_producto})
            
            if not resultado_producto.first():
                await self.db.rollback()
                raise ExcepcionNoEncontrado("Producto")
            
            query_detalle = text("""
                INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_unitario)
                VALUES (:id_compra, :id_producto, :cantidad, :precio_unitario)
            """)
            await self.db.execute(query_detalle, {
                "id_compra": id_compra,
                "id_producto": detalle.id_producto,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario
            })
            
            query_actualizar = text("""
                UPDATE productos SET cantidad = cantidad + :cantidad WHERE id_producto = :id_producto
            """)
            await self.db.execute(query_actualizar, {
                "cantidad": detalle.cantidad,
                "id_producto": detalle.id_producto
            })
        
        await self.db.commit()
        return await self.obtener_por_id(id_compra)
    
    async def obtener_por_id(self, id_compra: int):
        query = text("""
            SELECT id_compra, id_proveedor, id_usuario, id_estado_compra, fecha_compra, hora_compra
            FROM compras
            WHERE id_compra = :id_compra
        """)
        resultado = await self.db.execute(query, {"id_compra": id_compra})
        compra = resultado.mappings().first()
        if not compra:
            raise ExcepcionNoEncontrado("Compra")
        return compra
    
    async def listar_por_usuario(self, id_usuario: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_compra, id_proveedor, id_usuario, id_estado_compra, fecha_compra, hora_compra
            FROM compras
            WHERE id_usuario = :id_usuario
            ORDER BY id_compra DESC
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
