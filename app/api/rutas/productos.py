from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.producto import ProductoCrear, ProductoRespuesta, TipoProductoCrear, TipoProductoRespuesta
from app.servicios.producto import ServicioProducto, ServicioTipoProducto

router = APIRouter()

@router.post("/tipos", response_model=TipoProductoRespuesta, status_code=201)
async def crear_tipo_producto(
    tipo: TipoProductoCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioTipoProducto(db)
    return await servicio.crear(tipo)

@router.get("/tipos", response_model=List[TipoProductoRespuesta])
async def listar_tipos_producto(
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioTipoProducto(db)
    return await servicio.listar_por_tenant(id_tenant)

@router.post("/", response_model=ProductoRespuesta, status_code=201)
async def crear_producto(
    producto: ProductoCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProducto(db)
    return await servicio.crear(producto)

@router.get("/", response_model=List[ProductoRespuesta])
async def listar_productos(
    id_tipo_producto: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProducto(db)
    return await servicio.listar_por_tipo(id_tipo_producto, skip, limit)

@router.get("/{id_producto}", response_model=ProductoRespuesta)
async def obtener_producto(
    id_producto: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProducto(db)
    return await servicio.obtener_por_id(id_producto)
