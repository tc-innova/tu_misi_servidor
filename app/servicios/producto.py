from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.esquemas.producto import ProductoCrear, ProductoActualizar, ProductoRespuesta
from app.nucleo.excepciones import ExcepcionNoEncontrado, ExcepcionConflicto

class ServicioProducto:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def crear(self, producto: ProductoCrear, id_tenant: int) -> ProductoRespuesta:
        query_verificar = text("""
            SELECT id_producto 
            FROM productos 
            WHERE id_tenant = :id_tenant AND codigo_barras = :codigo_barras
        """)
        
        resultado = await self.db.execute(
            query_verificar,
            {"id_tenant": id_tenant, "codigo_barras": producto.codigo_barras}
        )
        existente = resultado.first()
        
        if existente:
            raise ExcepcionConflicto(f"El producto con código '{producto.codigo_barras}' ya existe")

        query_insertar = text("""
            INSERT INTO productos (
                id_tenant, id_tipo_producto, codigo_barras, nombre, 
                precio, cantidad, cantidad_minima, activo
            )
            VALUES (
                :id_tenant, :id_tipo_producto, :codigo_barras, :nombre, 
                :precio, :cantidad, :cantidad_minima, :activo
            )
            RETURNING id_producto, id_tenant, id_tipo_producto, codigo_barras, 
                      nombre, precio, cantidad, cantidad_minima, activo
        """)
        
        resultado = await self.db.execute(query_insertar, {
            "id_tenant": id_tenant,
            "id_tipo_producto": producto.id_tipo_producto,
            "codigo_barras": producto.codigo_barras,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad,
            "cantidad_minima": producto.cantidad_minima,
            "activo": producto.activo
        })
        await self.db.commit()
        
        fila = resultado.mappings().first()
        return ProductoRespuesta(**fila)
    
    async def listar_por_tenant(
        self, 
        id_tenant: int, 
        id_tipo_producto: int = None,
        activo: bool = None,
        pagina: int = 1, 
        limite: int = 20
    ) -> list[ProductoRespuesta]:
        offset = (pagina - 1) * limite
        
        condiciones = ["id_tenant = :id_tenant"]
        parametros = {"id_tenant": id_tenant, "offset": offset, "limite": limite}
        
        if id_tipo_producto is not None:
            condiciones.append("id_tipo_producto = :id_tipo_producto")
            parametros["id_tipo_producto"] = id_tipo_producto
        
        if activo is not None:
            condiciones.append("activo = :activo")
            parametros["activo"] = activo
        
        where_clause = " AND ".join(condiciones)
        
        query = text(f"""
            SELECT id_producto, id_tenant, id_tipo_producto, codigo_barras, 
                   nombre, precio, cantidad, cantidad_minima, activo
            FROM productos
            WHERE {where_clause}
            ORDER BY nombre
            OFFSET :offset LIMIT :limite
        """)
        
        resultado = await self.db.execute(query, parametros)
        return [ProductoRespuesta(**fila) for fila in resultado.mappings().all()]
    
    async def obtener_por_id(self, id_producto: int) -> ProductoRespuesta:
        query = text("""
            SELECT id_producto, id_tenant, id_tipo_producto, codigo_barras, 
                   nombre, precio, cantidad, cantidad_minima, activo
            FROM productos
            WHERE id_producto = :id_producto
        """)
        
        resultado = await self.db.execute(query, {"id_producto": id_producto})
        fila = resultado.mappings().first()
        
        if not fila:
            raise ExcepcionNoEncontrado("Producto no encontrado")
        
        return ProductoRespuesta(**fila)
    
    async def actualizar(
        self,
        id_producto: int,
        datos: ProductoActualizar
    ) -> ProductoRespuesta:
        await self.obtener_por_id(id_producto)
        
        campos_actualizar = datos.model_dump(exclude_unset=True)
        
        if not campos_actualizar:
            return await self.obtener_por_id(id_producto)
        
        set_clause = ", ".join([f"{campo} = :{campo}" for campo in campos_actualizar.keys()])
        
        query = text(f"""
            UPDATE productos
            SET {set_clause}
            WHERE id_producto = :id_producto
            RETURNING id_producto, id_tenant, id_tipo_producto, codigo_barras, 
                      nombre, precio, cantidad, cantidad_minima, activo
        """)
        
        parametros = {**campos_actualizar, "id_producto": id_producto}
        resultado = await self.db.execute(query, parametros)
        await self.db.commit()
        
        fila = resultado.mappings().first()
        return ProductoRespuesta(**fila)
    
    async def eliminar(self, id_producto: int):
        await self.obtener_por_id(id_producto)
        
        query = text("""
            DELETE FROM productos
            WHERE id_producto = :id_producto
        """)
        
        await self.db.execute(query, {"id_producto": id_producto})
        await self.db.commit()

