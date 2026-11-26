from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_administrador_actual
from app.nucleo.respuestas import RESPUESTAS_CREAR, RESPUESTAS_LISTAR, RESPUESTAS_OBTENER, RESPUESTAS_ELIMINAR
from app.esquemas.tenant import TenantCrear, TenantRespuesta
from app.servicios.tenant import ServicioTenant
from app.servicios.usuario import ServicioUsuario

router = APIRouter()

@router.post(
    "/",
    response_model=TenantRespuesta,
    status_code=201,
    responses=RESPUESTAS_CREAR
)
async def crear_tenant(
    tenant: TenantCrear,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioTenant(db)
    return await servicio.crear(tenant)

@router.get(
    "/",
    response_model=List[TenantRespuesta],
    responses=RESPUESTAS_LISTAR
)
async def listar_tenants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioTenant(db)
    return await servicio.listar(skip, limit)

@router.get(
    "/{id_tenant}",
    response_model=TenantRespuesta,
    responses=RESPUESTAS_OBTENER
)
async def obtener_tenant(
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioTenant(db)
    return await servicio.obtener_por_id(id_tenant)

@router.get(
    "/usuarios/{id_usuario}",
    response_model=List[dict],
    responses=RESPUESTAS_LISTAR
)
async def listar_tenants_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_tenants_usuario(id_usuario)

@router.post(
    "/usuarios/{id_usuario}/{id_tenant}",
    status_code=201,
    responses=RESPUESTAS_CREAR
)
async def agregar_tenant_usuario(
    id_usuario: int,
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.agregar_tenant_usuario(id_usuario, id_tenant)

@router.delete(
    "/usuarios/{id_usuario}/{id_tenant}",
    status_code=204,
    responses=RESPUESTAS_ELIMINAR
)
async def remover_tenant_usuario(
    id_usuario: int,
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    await servicio.remover_tenant_usuario(id_usuario, id_tenant)

