from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.tenant import TenantCrear, TenantRespuesta
from app.servicios.tenant import ServicioTenant

router = APIRouter()

@router.post("/", response_model=TenantRespuesta, status_code=201)
async def crear_tenant(
    tenant: TenantCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioTenant(db)
    return await servicio.crear(tenant)

@router.get("/", response_model=List[TenantRespuesta])
async def listar_tenants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioTenant(db)
    return await servicio.listar(skip, limit)

@router.get("/{id_tenant}", response_model=TenantRespuesta)
async def obtener_tenant(
    id_tenant: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioTenant(db)
    return await servicio.obtener_por_id(id_tenant)
