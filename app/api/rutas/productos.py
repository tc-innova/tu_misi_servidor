from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_usuario_actual
from app.esquemas.producto import ProductoCrear, ProductoActualizar, ProductoRespuesta
from app.servicios.producto import ServicioProducto

router = APIRouter()

@router.post("/", response_model=ProductoRespuesta, status_code=201)
async def crear_producto(
    producto: ProductoCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    servicio = ServicioProducto(db)
    return await servicio.crear(producto, usuario["id_tenant"])

@router.get("/", response_model=List[ProductoRespuesta])
async def listar_productos(
    id_tipo_producto: int = None,
    activo: bool = None,
    pagina: int = 1,
    limite: int = 20,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    servicio = ServicioProducto(db)
    return await servicio.listar_por_tenant(
        usuario["id_tenant"],
        id_tipo_producto,
        activo,
        pagina,
        limite
    )

@router.get("/{id_producto}", response_model=ProductoRespuesta)
async def obtener_producto(
    id_producto: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    servicio = ServicioProducto(db)
    producto = await servicio.obtener_por_id(id_producto)
    
    if producto.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes acceder a productos de otro tenant"
        )
    
    return producto

@router.put("/{id_producto}", response_model=ProductoRespuesta)
async def actualizar_producto(
    id_producto: int,
    datos: ProductoActualizar,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    servicio = ServicioProducto(db)
    producto_existente = await servicio.obtener_por_id(id_producto)
    
    if producto_existente.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes editar productos de otro tenant"
        )
    
    return await servicio.actualizar(id_producto, datos)

@router.delete("/{id_producto}", status_code=204)
async def eliminar_producto(
    id_producto: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(obtener_usuario_actual)
):
    servicio = ServicioProducto(db)
    producto_existente = await servicio.obtener_por_id(id_producto)
    
    if producto_existente.id_tenant != usuario["id_tenant"]:
        raise HTTPException(
            status_code=403,
            detail="No puedes eliminar productos de otro tenant"
        )
    
    await servicio.eliminar(id_producto)

