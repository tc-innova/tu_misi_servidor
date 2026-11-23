from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_usuario_actual
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
    if tipo_producto.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes crear categorías para otro tenant"
        )
    
    servicio = ServicioTipoProducto(db)
    return await servicio.crear(tipo_producto)

@router.get("/", response_model=List[TipoProductoRespuesta])
async def listar_tipos_productos(
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Lista los tipos de productos del tenant del usuario autenticado.
    Cada usuario solo ve las categorías de su propio tenant.
    """
    servicio = ServicioTipoProducto(db)
    return await servicio.listar_por_tenant(usuario["id_tenant"])

@router.get("/{id_tipo_producto}", response_model=TipoProductoRespuesta)
async def obtener_tipo_producto(
    id_tipo_producto: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Obtiene un tipo de producto específico.
    Solo puede ver si pertenece a su tenant.
    """
    servicio = ServicioTipoProducto(db)
    tipo_producto = await servicio.obtener_por_id(id_tipo_producto)
    
    if tipo_producto.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes acceder a categorías de otro tenant"
        )
    
    return tipo_producto

@router.put("/{id_tipo_producto}", response_model=TipoProductoRespuesta)
async def actualizar_tipo_producto(
    id_tipo_producto: int,
    datos: TipoProductoActualizar,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    """
    Actualiza un tipo de producto.
    Solo puede editar categorías de su propio tenant.
    """
    servicio = ServicioTipoProducto(db)
    tipo_existente = await servicio.obtener_por_id(id_tipo_producto)
    
    if tipo_existente.id_tenant != usuario["id_tenant"]:
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
    Elimina un tipo de producto.
    Solo puede eliminar categorías de su propio tenant.
    """
    servicio = ServicioTipoProducto(db)
    tipo_existente = await servicio.obtener_por_id(id_tipo_producto)
    
    if tipo_existente.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes eliminar categorías de otro tenant"
        )
    
    await servicio.eliminar(id_tipo_producto)

