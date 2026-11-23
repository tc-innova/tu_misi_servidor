from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modelos.tipo_producto import TipoProducto
from app.esquemas.tipo_producto import TipoProductoCrear, TipoProductoActualizar
from app.nucleo.excepciones import ExcepcionNoEncontrado, ExcepcionConflicto

class ServicioTipoProducto:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, tipo_producto: TipoProductoCrear) -> TipoProducto:
        # Verificar si ya existe el nombre para ese tenant
        query = select(TipoProducto).where(
            TipoProducto.id_tenant == tipo_producto.id_tenant,
            TipoProducto.nombre == tipo_producto.nombre
        )
        resultado = await self.db.execute(query)
        existente = resultado.scalar_one_or_none()
        
        if existente:
            raise ExcepcionConflicto(f"El tipo de producto '{tipo_producto.nombre}' ya existe")

        nuevo_tipo = TipoProducto(**tipo_producto.model_dump())
        self.db.add(nuevo_tipo)
        await self.db.commit()
        await self.db.refresh(nuevo_tipo)
        return nuevo_tipo

    async def listar_por_tenant(self, id_tenant: int) -> list[TipoProducto]:
        query = select(TipoProducto).where(
            TipoProducto.id_tenant == id_tenant
        ).order_by(TipoProducto.nombre)
        
        resultado = await self.db.execute(query)
        return list(resultado.scalars().all())

    async def obtener_por_id(self, id_tipo_producto: int) -> TipoProducto:
        query = select(TipoProducto).where(
            TipoProducto.id_tipo_producto == id_tipo_producto
        )
        resultado = await self.db.execute(query)
        tipo_producto = resultado.scalar_one_or_none()
        
        if not tipo_producto:
            raise ExcepcionNoEncontrado("Tipo de producto no encontrado")
        
        return tipo_producto

    async def actualizar(
        self,
        id_tipo_producto: int,
        datos: TipoProductoActualizar
    ) -> TipoProducto:
        tipo_producto = await self.obtener_por_id(id_tipo_producto)
        
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(tipo_producto, campo, valor)
        
        await self.db.commit()
        await self.db.refresh(tipo_producto)
        return tipo_producto

    async def eliminar(self, id_tipo_producto: int):
        tipo_producto = await self.obtener_por_id(id_tipo_producto)
        await self.db.delete(tipo_producto)
        await self.db.commit()
