from pydantic import BaseModel
from typing import Optional

class TipoProductoBase(BaseModel):
    nombre: str

class TipoProductoCrear(TipoProductoBase):
    id_tenant: int

class TipoProductoActualizar(BaseModel):
    nombre: Optional[str] = None

class TipoProductoRespuesta(TipoProductoBase):
    id_tipo_producto: int
    id_tenant: int
    
    class Config:
        from_attributes = True
