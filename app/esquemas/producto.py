from pydantic import BaseModel
from decimal import Decimal

class TipoProductoBase(BaseModel):
    nombre: str

class TipoProductoCrear(TipoProductoBase):
    id_tenant: int

class TipoProductoRespuesta(TipoProductoBase):
    id_tipo_producto: int
    id_tenant: int
    
    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    precio: Decimal
    cantidad: int
    cantidad_minima: int
    activo: bool = True

class ProductoCrear(ProductoBase):
    id_tipo_producto: int

class ProductoRespuesta(ProductoBase):
    id_producto: int
    id_tipo_producto: int
    
    class Config:
        from_attributes = True
