from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_usuario_temporal
from app.nucleo.seguridad import verificar_token
from app.esquemas.autenticacion import (
    LoginCredenciales,
    TokenTemporal,
    TenantDisponible,
    SeleccionTenant,
    TokenAcceso,
    TokenRefrescado
)
from app.servicios.autenticacion import ServicioAutenticacion

router = APIRouter()

@router.post("/login/admin", response_model=TokenAcceso)
async def login_admin(
    credenciales: LoginCredenciales,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.login_admin(
        credenciales.usuario,
        credenciales.contrasenia
    )

@router.post("/login/cliente", response_model=TokenTemporal)
async def login_cliente(
    credenciales: LoginCredenciales,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.login_credenciales(
        credenciales.usuario,
        credenciales.contrasenia
    )

@router.get("/tenants", response_model=List[TenantDisponible])
async def listar_tenants(
    usuario_temporal = Depends(obtener_usuario_temporal),
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    tenants = await servicio.listar_tenants_usuario(usuario_temporal["id_usuario"])
    
    if not tenants:
        raise HTTPException(
            status_code=404,
            detail="No tienes acceso a ningún negocio"
        )
    
    return tenants

@router.post("/tenant/select", response_model=TokenAcceso)
async def seleccionar_tenant(
    seleccion: SeleccionTenant,
    usuario_temporal = Depends(obtener_usuario_temporal),
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.seleccionar_tenant(
        usuario_temporal["id_usuario"],
        seleccion.id_tenant
    )

@router.post("/refresh", response_model=TokenRefrescado)
async def refrescar_token(
    token_refresco: str,
    db: AsyncSession = Depends(obtener_db)
):
    payload = verificar_token(token_refresco)
    
    if not payload or payload.get("tipo") != "refresco":
        raise HTTPException(
            status_code=401,
            detail="Token de refresco inválido"
        )
    
    id_usuario = payload.get("id_usuario")
    id_tenant = payload.get("id_tenant")
    
    if not id_usuario or not id_tenant:
        raise HTTPException(
            status_code=401,
            detail="Token incompleto"
        )
    
    servicio = ServicioAutenticacion(db)
    return await servicio.refrescar_token(id_usuario, id_tenant)
