from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductoBase(BaseModel):
    codigo_barras: Optional[str] = None
    nombre: str
    precio: Decimal
    cantidad: int
    cantidad_minima: int
    activo: bool = True

class ProductoCrear(ProductoBase):
    id_tipo_producto: int

class ProductoActualizar(BaseModel):
    id_tipo_producto: Optional[int] = None
    codigo_barras: Optional[str] = None
    nombre: Optional[str] = None
    precio: Optional[Decimal] = None
    cantidad: Optional[int] = None
    cantidad_minima: Optional[int] = None
    activo: Optional[bool] = None

class ProductoRespuesta(ProductoBase):
    id_producto: int
    id_tenant: int
    id_tipo_producto: int
    
    class Config:
        from_attributes = True

