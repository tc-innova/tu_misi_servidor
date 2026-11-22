from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.nucleo.base_datos import obtener_db
from app.nucleo.permisos import requiere_roles
from app.esquemas.venta import VentaCrear, VentaRespuesta
from app.servicios.venta import ServicioVenta

router = APIRouter()

@router.post("/", response_model=VentaRespuesta, status_code=201)
async def crear_venta(
    venta: VentaCrear,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioVenta(db)
    return await servicio.crear(venta)

@router.get("/", response_model=List[VentaRespuesta])
async def listar_ventas(
    id_usuario: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioVenta(db)
    return await servicio.listar_por_usuario(id_usuario, skip, limit)

@router.get("/{id_venta}", response_model=VentaRespuesta)
async def obtener_venta(
    id_venta: int,
    db: AsyncSession = Depends(obtener_db),
    usuario = Depends(requiere_roles("administrador", "cliente"))
):
    servicio = ServicioVenta(db)
    return await servicio.obtener_por_id(id_venta)
