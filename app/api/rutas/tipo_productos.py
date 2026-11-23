from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.nucleo.autenticacion import obtener_usuario_actual
from app.nucleo.limitador import limiter
from app.esquemas.tipo_producto import (
    TipoProductoCrear,
    TipoProductoActualizar,
    TipoProductoRespuesta
)
from app.servicios.tipo_producto import ServicioTipoProducto

router = APIRouter()

@router.post("/", response_model=TipoProductoRespuesta, status_code=201)
async def crear_tipo_producto(
    tipo_producto: TipoProductoCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Clientes autenticados pueden crear tipos de productos para su tenant.
    El id_tenant del tipo de producto debe coincidir con el id_tenant del usuario.
    """
    # Validar que el usuario esté creando categorías para su propio tenant
    if tipo_producto.id_tenant != usuario.id_tenant:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="No puedes crear categorías para otro tenant"
        )
    
    servicio = ServicioTipoProducto(db)
    return await servicio.crear(tipo_producto)

@router.get("/", response_model=List[TipoProductoRespuesta])
async def listar_tipos_productos(
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db)
):
    """
    Ruta pública - Los clientes pueden ver las categorías para filtrar productos.
    No requiere autenticación.
    """
    servicio = ServicioTipoProducto(db)
    return await servicio.listar_por_tenant(id_tenant)

@router.get("/{id_tipo_producto}", response_model=TipoProductoRespuesta)
async def obtener_tipo_producto(
    id_tipo_producto: int,
    db: AsyncSession = Depends(obtener_db)
):
    """Ruta pública - Cualquiera puede ver un tipo de producto específico"""
    servicio = ServicioTipoProducto(db)
    return await servicio.obtener_por_id(id_tipo_producto)

@router.put("/{id_tipo_producto}", response_model=TipoProductoRespuesta)
async def actualizar_tipo_producto(
    id_tipo_producto: int,
    datos: TipoProductoActualizar,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Clientes autenticados pueden actualizar sus propios tipos de productos.
    Solo se pueden editar categorías del mismo tenant.
    """
    servicio = ServicioTipoProducto(db)
    
    # Obtener el tipo de producto para validar tenant
    tipo_existente = await servicio.obtener_por_id(id_tipo_producto)
    if tipo_existente.id_tenant != usuario.id_tenant:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="No puedes editar categorías de otro tenant"
        )
    
    return await servicio.actualizar(id_tipo_producto, datos)

@router.delete("/{id_tipo_producto}", status_code=204)
async def eliminar_tipo_producto(
    id_tipo_producto: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Clientes autenticados pueden eliminar sus propios tipos de productos.
    Solo se pueden eliminar categorías del mismo tenant.
    """
    servicio = ServicioTipoProducto(db)
    
    # Obtener el tipo de producto para validar tenant
    tipo_existente = await servicio.obtener_por_id(id_tipo_producto)
    if tipo_existente.id_tenant != usuario.id_tenant:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="No puedes eliminar categorías de otro tenant"
        )
    
    await servicio.eliminar(id_tipo_producto)
