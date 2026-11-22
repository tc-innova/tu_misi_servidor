from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.nucleo.limitador import limiter
from app.esquemas.usuario import (
    UsuarioCrear, UsuarioRespuesta, UsuarioAdministradorCrear, UsuarioClienteCrear,
    CelularBase, CelularRespuesta, CorreoBase, CorreoRespuesta
)
from app.servicios.usuario import ServicioUsuario

router = APIRouter()

@router.post("/administrador", response_model=UsuarioRespuesta, status_code=201)
@limiter.limit("3/minute")
async def crear_usuario_administrador(
    request: Request,
    usuario: UsuarioAdministradorCrear,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioUsuario(db)
    id_rol_admin = await servicio.obtener_id_rol_por_nombre("administrador")
    return await servicio.crear(usuario, id_rol_admin)

@router.post("/cliente", response_model=UsuarioRespuesta, status_code=201)
@limiter.limit("5/minute")
async def crear_usuario_cliente(
    request: Request,
    usuario: UsuarioClienteCrear,
    db: AsyncSession = Depends(obtener_db)
):
    servicio = ServicioUsuario(db)
    id_rol_cliente = await servicio.obtener_id_rol_por_nombre("cliente")
    return await servicio.crear(usuario, id_rol_cliente)

@router.post("/", response_model=UsuarioRespuesta, status_code=201)
async def crear_usuario(
    usuario: UsuarioCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario_actual = Depends(requiere_roles("administrador"))
):
    servicio = ServicioUsuario(db)
    return await servicio.crear(usuario)

@router.post("/{id_usuario}/celulares", response_model=CelularRespuesta, status_code=201)
async def agregar_celular_usuario(
    id_usuario: int,
    celular: CelularBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    return await servicio.agregar_celular(id_usuario, celular)

@router.post("/{id_usuario}/correos", response_model=CorreoRespuesta, status_code=201)
async def agregar_correo_usuario(
    id_usuario: int,
    correo: CorreoBase,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    return await servicio.agregar_correo(id_usuario, correo)

@router.get("/{id_usuario}/celulares", response_model=List[CelularRespuesta])
async def listar_celulares_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_celulares(id_usuario)

@router.get("/{id_usuario}/correos", response_model=List[CorreoRespuesta])
async def listar_correos_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_correos(id_usuario)

@router.delete("/celulares/{id_celular}", status_code=204)
async def eliminar_celular_usuario(
    id_celular: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    await servicio.eliminar_celular(id_celular)

@router.delete("/correos/{id_correo}", status_code=204)
async def eliminar_correo_usuario(
    id_correo: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    await servicio.eliminar_correo(id_correo)

@router.get("/", response_model=List[UsuarioRespuesta])
async def listar_usuarios(
    id_tenant: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioUsuario(db)
    return await servicio.listar_por_tenant(id_tenant, skip, limit)

@router.get("/{id_usuario}", response_model=UsuarioRespuesta)
async def obtener_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioUsuario(db)
    return await servicio.obtener_por_id(id_usuario)
