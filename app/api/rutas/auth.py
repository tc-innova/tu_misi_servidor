from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.nucleo.base_datos import obtener_db
from app.nucleo.seguridad import verificar_token
from app.nucleo.respuestas import RESPUESTAS_AUTH
from app.esquemas.autenticacion import (
    LoginCredenciales,
    TokenAcceso,
    TokenConRefresco,
    TokenRefrescado,
    SeleccionarTenant
)
from app.nucleo.autenticacion import obtener_usuario_actual
from app.servicios.autenticacion import ServicioAutenticacion

router = APIRouter()

@router.post(
    "/login/admin",
    response_model=TokenAcceso,
    responses=RESPUESTAS_AUTH
)
async def login_admin(
    credenciales: LoginCredenciales,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.login_admin(
        credenciales.usuario,
        credenciales.contrasenia
    )

@router.post(
    "/login/usuario",
    response_model=TokenConRefresco,
    responses=RESPUESTAS_AUTH
)
async def login_usuario(
    credenciales: LoginCredenciales,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.login_usuario(
        credenciales.usuario,
        credenciales.contrasenia
    )

@router.post(
    "/refresh",
    response_model=TokenRefrescado,
    responses=RESPUESTAS_AUTH
)
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
    
    if not id_usuario:
        raise HTTPException(
            status_code=401,
            detail="Token incompleto"
        )
    
    servicio = ServicioAutenticacion(db)
    return await servicio.refrescar_token(id_usuario)

@router.post(
    "/select-tenant",
    response_model=TokenAcceso,
    responses=RESPUESTAS_AUTH
)
async def seleccionar_tenant(
    datos: SeleccionarTenant,
    usuario_actual: dict = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioAutenticacion(db)
    return await servicio.seleccionar_tenant(
        usuario_actual["id_usuario"],
        datos.id_tenant
    )
