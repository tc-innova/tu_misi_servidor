from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_administrador_actual
from app.nucleo.respuestas import RESPUESTAS_LISTAR, RESPUESTAS_ASIGNAR, RESPUESTAS_ELIMINAR
from app.esquemas.usuario import RolRespuesta
from app.servicios.usuario import ServicioUsuario

router = APIRouter()

@router.get(
    "/disponibles",
    response_model=List[RolRespuesta],
    responses=RESPUESTAS_LISTAR
)
async def listar_roles_disponibles(
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_roles_disponibles()

@router.get(
    "/usuarios/{id_usuario}",
    response_model=List[dict],
    responses=RESPUESTAS_LISTAR
)
async def listar_roles_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_roles_usuario(id_usuario)

@router.post(
    "/usuarios/{id_usuario}",
    status_code=201,
    responses=RESPUESTAS_ASIGNAR
)
async def asignar_rol_usuario(
    id_usuario: int,
    id_tenant: int,
    id_rol: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.asignar_rol(id_usuario, id_tenant, id_rol)

@router.delete(
    "/usuarios/{id_usuario}/{id_rol}",
    status_code=204,
    responses=RESPUESTAS_ELIMINAR
)
async def remover_rol_usuario(
    id_usuario: int,
    id_rol: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    await servicio.remover_rol(id_usuario, id_rol)
