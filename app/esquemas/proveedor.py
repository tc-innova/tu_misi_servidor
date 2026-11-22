from pydantic import BaseModel
from typing import Optional

class TipoProveedorBase(BaseModel):
    nombre: str

class TipoProveedorCrear(TipoProveedorBase):
    id_tenant: int

class TipoProveedorRespuesta(TipoProveedorBase):
    id_tipo_proveedor: int
    id_tenant: int
    
    class Config:
        from_attributes = True

class CelularProveedorBase(BaseModel):
    codigo_pais: str
    numero: str

class CelularProveedorRespuesta(CelularProveedorBase):
    id_celular: int
    id_proveedor: int
    
    class Config:
        from_attributes = True

class CorreoProveedorBase(BaseModel):
    correo: str

class CorreoProveedorRespuesta(CorreoProveedorBase):
    id_correo: int
    id_proveedor: int
    
    class Config:
        from_attributes = True

class ProveedorBase(BaseModel):
    nombre: str
    activo: bool = True

class ProveedorCrear(ProveedorBase):
    id_tenant: int
    id_tipo_proveedor: int

class ProveedorRespuesta(ProveedorBase):
    id_proveedor: int
    id_tenant: int
    id_tipo_proveedor: int
    
    class Config:
        from_attributes = True
