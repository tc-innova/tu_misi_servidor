from fastapi import APIRouter
from app.api.rutas import (
    auth,
    tenants,
    usuarios,
    clientes,
    proveedores,
    productos,
    tipo_productos,
    ventas,
    compras
)

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
router.include_router(proveedores.router, prefix="/proveedores", tags=["Proveedores"])
router.include_router(tipo_productos.router, prefix="/tipo-productos", tags=["Tipo Productos"])
router.include_router(productos.router, prefix="/productos", tags=["Productos"])
router.include_router(ventas.router, prefix="/ventas", tags=["Ventas"])
router.include_router(compras.router, prefix="/compras", tags=["Compras"])

