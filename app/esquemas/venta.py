from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal
from typing import Optional, List

class EstadoVentaBase(BaseModel):
    nombre: str

class EstadoVentaRespuesta(EstadoVentaBase):
    id_estado_venta: int
    
    class Config:
        from_attributes = True

class DetalleVentaBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal

class VentaBase(BaseModel):
    id_cliente: Optional[int] = None
    id_usuario: int
    id_estado_venta: int
    fecha_venta: date
    hora_venta: time

class VentaCrear(VentaBase):
    detalles: List[DetalleVentaBase]

class VentaRespuesta(VentaBase):
    id_venta: int
    
    class Config:
        from_attributes = True
