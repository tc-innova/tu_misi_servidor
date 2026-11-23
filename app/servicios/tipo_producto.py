from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.esquemas.tipo_producto import TipoProductoCrear, TipoProductoActualizar, TipoProductoRespuesta
from app.nucleo.excepciones import ExcepcionNoEncontrado, ExcepcionConflicto

class ServicioTipoProducto:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, tipo_producto: TipoProductoCrear) -> TipoProductoRespuesta:
        # Verificar si ya existe el nombre para ese tenant
        query_verificar = text("""
            SELECT id_tipo_producto 
            FROM tipo_productos 
            WHERE id_tenant = :id_tenant AND nombre = :nombre
        """)
        
        resultado = await self.db.execute(
            query_verificar,
            {"id_tenant": tipo_producto.id_tenant, "nombre": tipo_producto.nombre}
        )
        existente = resultado.first()
        
        if existente:
            raise ExcepcionConflicto(f"El tipo de producto '{tipo_producto.nombre}' ya existe")

        # Insertar nuevo tipo de producto
        query_insertar = text("""
            INSERT INTO tipo_productos (id_tenant, nombre)
            VALUES (:id_tenant, :nombre)
            RETURNING id_tipo_producto, id_tenant, nombre
        """)
        
        resultado = await self.db.execute(
            query_insertar,
            tipo_producto.model_dump()
        )
        await self.db.commit()
        
        fila = resultado.mappings().first()
        return TipoProductoRespuesta(**fila)

    async def listar_por_tenant(self, id_tenant: int) -> list[TipoProductoRespuesta]:
        query = text("""
            SELECT id_tipo_producto, id_tenant, nombre
            FROM tipo_productos
            WHERE id_tenant = :id_tenant
            ORDER BY nombre
        """)
        
        resultado = await self.db.execute(query, {"id_tenant": id_tenant})
        return [TipoProductoRespuesta(**fila) for fila in resultado.mappings().all()]

    async def obtener_por_id(self, id_tipo_producto: int) -> TipoProductoRespuesta:
        query = text("""
            SELECT id_tipo_producto, id_tenant, nombre
            FROM tipo_productos
            WHERE id_tipo_producto = :id_tipo_producto
        """)
        
        resultado = await self.db.execute(query, {"id_tipo_producto": id_tipo_producto})
        fila = resultado.mappings().first()
        
        if not fila:
            raise ExcepcionNoEncontrado("Tipo de producto no encontrado")
        
        return TipoProductoRespuesta(**fila)

    async def actualizar(
        self,
        id_tipo_producto: int,
        datos: TipoProductoActualizar
    ) -> TipoProductoRespuesta:
        # Verificar que existe
        await self.obtener_por_id(id_tipo_producto)
        
        # Construir UPDATE dinámico solo con campos proporcionados
        campos_actualizar = datos.model_dump(exclude_unset=True)
        
        if not campos_actualizar:
            return await self.obtener_por_id(id_tipo_producto)
        
        set_clause = ", ".join([f"{campo} = :{campo}" for campo in campos_actualizar.keys()])
        
        query = text(f"""
            UPDATE tipo_productos
            SET {set_clause}
            WHERE id_tipo_producto = :id_tipo_producto
            RETURNING id_tipo_producto, id_tenant, nombre
        """)
        
        parametros = {**campos_actualizar, "id_tipo_producto": id_tipo_producto}
        resultado = await self.db.execute(query, parametros)
        await self.db.commit()
        
        fila = resultado.mappings().first()
        return TipoProductoRespuesta(**fila)

    async def eliminar(self, id_tipo_producto: int):
        # Verificar que existe
        await self.obtener_por_id(id_tipo_producto)
        
        query = text("""
            DELETE FROM tipo_productos
            WHERE id_tipo_producto = :id_tipo_producto
        """)
        
        await self.db.execute(query, {"id_tipo_producto": id_tipo_producto})
        await self.db.commit()

