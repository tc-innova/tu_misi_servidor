from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.compra import CompraCrear, CompraRespuesta
from app.servicios.compra import ServicioCompra

router = APIRouter()

@router.post("/", response_model=CompraRespuesta, status_code=201)
async def crear_compra(
    compra: CompraCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioCompra(db)
    return await servicio.crear(compra)

@router.get("/", response_model=List[CompraRespuesta])
async def listar_compras(
    id_usuario: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioCompra(db)
    return await servicio.listar_por_usuario(id_usuario, skip, limit)

@router.get("/{id_compra}", response_model=CompraRespuesta)
async def obtener_compra(
    id_compra: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador"))
):
    servicio = ServicioCompra(db)
    return await servicio.obtener_por_id(id_compra)
