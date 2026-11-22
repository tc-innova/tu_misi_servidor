from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.cliente import (
    ClienteCrear, ClienteRespuesta,
    CelularClienteBase, CelularClienteRespuesta,
    CorreoClienteBase, CorreoClienteRespuesta
)
from app.servicios.cliente import ServicioCliente

router = APIRouter()

@router.post("/", response_model=ClienteRespuesta, status_code=201)
async def crear_cliente(
    cliente: ClienteCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.crear(cliente)

@router.post("/{id_cliente}/celulares", response_model=CelularClienteRespuesta, status_code=201)
async def agregar_celular_cliente(
    id_cliente: int,
    celular: CelularClienteBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.agregar_celular(id_cliente, celular)

@router.post("/{id_cliente}/correos", response_model=CorreoClienteRespuesta, status_code=201)
async def agregar_correo_cliente(
    id_cliente: int,
    correo: CorreoClienteBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.agregar_correo(id_cliente, correo)

@router.get("/{id_cliente}/celulares", response_model=List[CelularClienteRespuesta])
async def listar_celulares_cliente(
    id_cliente: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.listar_celulares(id_cliente)

@router.get("/{id_cliente}/correos", response_model=List[CorreoClienteRespuesta])
async def listar_correos_cliente(
    id_cliente: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.listar_correos(id_cliente)

@router.delete("/celulares/{id_celular}", status_code=204)
async def eliminar_celular_cliente(
    id_celular: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    await servicio.eliminar_celular(id_celular)

@router.delete("/correos/{id_correo}", status_code=204)
async def eliminar_correo_cliente(
    id_correo: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    await servicio.eliminar_correo(id_correo)

@router.get("/", response_model=List[ClienteRespuesta])
async def listar_clientes(
    id_tenant: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.listar_por_tenant(id_tenant, skip, limit)

@router.get("/{id_cliente}", response_model=ClienteRespuesta)
async def obtener_cliente(
    id_cliente: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioCliente(db)
    return await servicio.obtener_por_id(id_cliente)
