from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal
from typing import Optional, List

class EstadoCompraBase(BaseModel):
    nombre: str

class EstadoCompraRespuesta(EstadoCompraBase):
    id_estado_compra: int
    
    class Config:
        from_attributes = True

class DetalleCompraBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal

class CompraBase(BaseModel):
    id_proveedor: Optional[int] = None
    id_usuario: int
    id_estado_compra: int
    fecha_compra: date
    hora_compra: time

class CompraCrear(CompraBase):
    detalles: List[DetalleCompraBase]

class CompraRespuesta(CompraBase):
    id_compra: int
    
    class Config:
        from_attributes = True
