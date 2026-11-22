from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.excepciones import ExcepcionNoEncontrado, ExcepcionInventarioInsuficiente
from app.nucleo.auditoria import auditar

class ServicioVenta:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @auditar("ventas", "crear")
    async def crear(self, venta):
        query_venta = text("""
            INSERT INTO ventas (id_cliente, id_usuario, id_estado_venta, fecha_venta, hora_venta)
            VALUES (:id_cliente, :id_usuario, :id_estado_venta, :fecha_venta, :hora_venta)
            RETURNING id_venta
        """)
        
        resultado = await self.db.execute(query_venta, {
            "id_cliente": venta.id_cliente,
            "id_usuario": venta.id_usuario,
            "id_estado_venta": venta.id_estado_venta,
            "fecha_venta": venta.fecha_venta,
            "hora_venta": venta.hora_venta
        })
        id_venta = resultado.scalar()
        
        for detalle in venta.detalles:
            query_producto = text("""
                SELECT nombre, cantidad FROM productos WHERE id_producto = :id_producto
            """)
            resultado_producto = await self.db.execute(query_producto, {"id_producto": detalle.id_producto})
            producto = resultado_producto.mappings().first()
            
            if not producto:
                await self.db.rollback()
                raise ExcepcionNoEncontrado("Producto")
            
            if producto["cantidad"] < detalle.cantidad:
                await self.db.rollback()
                raise ExcepcionInventarioInsuficiente(producto["nombre"])
            
            query_detalle = text("""
                INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario)
                VALUES (:id_venta, :id_producto, :cantidad, :precio_unitario)
            """)
            await self.db.execute(query_detalle, {
                "id_venta": id_venta,
                "id_producto": detalle.id_producto,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario
            })
            
            query_actualizar = text("""
                UPDATE productos SET cantidad = cantidad - :cantidad WHERE id_producto = :id_producto
            """)
            await self.db.execute(query_actualizar, {
                "cantidad": detalle.cantidad,
                "id_producto": detalle.id_producto
            })
        
        await self.db.commit()
        return await self.obtener_por_id(id_venta)
    
    async def obtener_por_id(self, id_venta: int):
        query = text("""
            SELECT id_venta, id_cliente, id_usuario, id_estado_venta, fecha_venta, hora_venta
            FROM ventas
            WHERE id_venta = :id_venta
        """)
        resultado = await self.db.execute(query, {"id_venta": id_venta})
        venta = resultado.mappings().first()
        if not venta:
            raise ExcepcionNoEncontrado("Venta")
        return venta
    
    async def listar_por_usuario(self, id_usuario: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_venta, id_cliente, id_usuario, id_estado_venta, fecha_venta, hora_venta
            FROM ventas
            WHERE id_usuario = :id_usuario
            ORDER BY id_venta DESC
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
