from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.autenticacion import obtener_administrador_actual
from app.nucleo.limitador import limiter
from app.nucleo.respuestas import (
    RESPUESTAS_CREAR_PUBLICO,
    RESPUESTAS_CREAR,
    RESPUESTAS_LISTAR,
    RESPUESTAS_OBTENER,
    RESPUESTAS_ACTUALIZAR,
    RESPUESTAS_ELIMINAR,
    RESPUESTAS_ASIGNAR
)
from app.esquemas.usuario import (
    UsuarioCrear, UsuarioRespuesta, UsuarioClientePruebaCrear,
    CelularBase, CelularRespuesta, CorreoBase, CorreoRespuesta, RolRespuesta
)
from app.servicios.usuario import ServicioUsuario

router = APIRouter()

@router.post(
    "/admin-prueba",
    response_model=UsuarioRespuesta,
    status_code=201,
    responses=RESPUESTAS_CREAR_PUBLICO
)
@limiter.limit("3/minute")
async def crear_usuario_admin_prueba(
    request: Request,
    usuario: UsuarioClientePruebaCrear,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioUsuario(db)
    return await servicio.crear_admin_con_tenant(usuario, usuario.nombre_negocio)

@router.post(
    "/",
    response_model=UsuarioRespuesta,
    status_code=201,
    responses=RESPUESTAS_ASIGNAR
)
async def crear_usuario(
    usuario: UsuarioCrear,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.crear(usuario)

@router.post(
    "/{id_usuario}/celulares",
    response_model=CelularRespuesta,
    status_code=201,
    responses=RESPUESTAS_CREAR
)
async def agregar_celular_usuario(
    id_usuario: int,
    celular: CelularBase,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.agregar_celular(id_usuario, celular)

@router.post(
    "/{id_usuario}/correos",
    response_model=CorreoRespuesta,
    status_code=201,
    responses=RESPUESTAS_CREAR
)
async def agregar_correo_usuario(
    id_usuario: int,
    correo: CorreoBase,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.agregar_correo(id_usuario, correo)

@router.get(
    "/{id_usuario}/celulares",
    response_model=List[CelularRespuesta],
    responses=RESPUESTAS_LISTAR
)
async def listar_celulares_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_celulares(id_usuario)

@router.get(
    "/{id_usuario}/correos",
    response_model=List[CorreoRespuesta],
    responses=RESPUESTAS_LISTAR
)
async def listar_correos_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_correos(id_usuario)

@router.delete(
    "/celulares",
    status_code=204,
    responses=RESPUESTAS_ELIMINAR
)
async def eliminar_celular_usuario(
    id_usuario: int,
    codigo_pais: str,
    numero: str,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    await servicio.eliminar_celular(id_usuario, codigo_pais, numero)

@router.delete(
    "/correos",
    status_code=204,
    responses=RESPUESTAS_ELIMINAR
)
async def eliminar_correo_usuario(
    id_usuario: int,
    correo: str,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    await servicio.eliminar_correo(id_usuario, correo)



@router.get(
    "/",
    response_model=List[UsuarioRespuesta],
    responses=RESPUESTAS_LISTAR
)
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_todos(skip, limit)

@router.get(
    "/{id_usuario}",
    response_model=UsuarioRespuesta,
    responses=RESPUESTAS_OBTENER
)
async def obtener_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.obtener_por_id(id_usuario)

@router.put(
    "/{id_usuario}",
    response_model=UsuarioRespuesta,
    responses=RESPUESTAS_ACTUALIZAR
)
async def actualizar_usuario(
    id_usuario: int,
    datos: dict,
    db: AsyncSession = Depends(obtener_db),
    admin_actual = Depends(obtener_administrador_actual)
):
    servicio = ServicioUsuario(db)
    return await servicio.actualizar(id_usuario, datos)
