from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.proveedor import (
    ProveedorCrear, ProveedorRespuesta, TipoProveedorCrear, TipoProveedorRespuesta,
    CelularProveedorBase, CelularProveedorRespuesta,
    CorreoProveedorBase, CorreoProveedorRespuesta
)
from app.servicios.proveedor import ServicioProveedor, ServicioTipoProveedor

router = APIRouter()

@router.post("/tipos", response_model=TipoProveedorRespuesta, status_code=201)
async def crear_tipo_proveedor(
    tipo: TipoProveedorCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioTipoProveedor(db)
    return await servicio.crear(tipo)

@router.get("/tipos", response_model=List[TipoProveedorRespuesta])
async def listar_tipos_proveedor(
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioTipoProveedor(db)
    return await servicio.listar_por_tenant(id_tenant)

@router.post("/", response_model=ProveedorRespuesta, status_code=201)
async def crear_proveedor(
    proveedor: ProveedorCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProveedor(db)
    return await servicio.crear(proveedor)

@router.post("/{id_proveedor}/celulares", response_model=CelularProveedorRespuesta, status_code=201)
async def agregar_celular_proveedor(
    id_proveedor: int,
    celular: CelularProveedorBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProveedor(db)
    return await servicio.agregar_celular(id_proveedor, celular)

@router.post("/{id_proveedor}/correos", response_model=CorreoProveedorRespuesta, status_code=201)
async def agregar_correo_proveedor(
    id_proveedor: int,
    correo: CorreoProveedorBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProveedor(db)
    return await servicio.agregar_correo(id_proveedor, correo)

@router.get("/{id_proveedor}/celulares", response_model=List[CelularProveedorRespuesta])
async def listar_celulares_proveedor(
    id_proveedor: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProveedor(db)
    return await servicio.listar_celulares(id_proveedor)

@router.get("/{id_proveedor}/correos", response_model=List[CorreoProveedorRespuesta])
async def listar_correos_proveedor(
    id_proveedor: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProveedor(db)
    return await servicio.listar_correos(id_proveedor)

@router.delete("/celulares/{id_celular}", status_code=204)
async def eliminar_celular_proveedor(
    id_celular: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProveedor(db)
    await servicio.eliminar_celular(id_celular)

@router.delete("/correos/{id_correo}", status_code=204)
async def eliminar_correo_proveedor(
    id_correo: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioProveedor(db)
    await servicio.eliminar_correo(id_correo)

@router.get("/", response_model=List[ProveedorRespuesta])
async def listar_proveedores(
    id_tenant: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProveedor(db)
    return await servicio.listar_por_tenant(id_tenant, skip, limit)

@router.get("/{id_proveedor}", response_model=ProveedorRespuesta)
async def obtener_proveedor(
    id_proveedor: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioProveedor(db)
    return await servicio.obtener_por_id(id_proveedor)
