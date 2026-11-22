from pydantic import BaseModel
from typing import Optional

class CelularClienteBase(BaseModel):
    codigo_pais: str
    numero: str

class CelularClienteRespuesta(CelularClienteBase):
    id_celular: int
    id_cliente: int
    
    class Config:
        from_attributes = True

class CorreoClienteBase(BaseModel):
    correo: str

class CorreoClienteRespuesta(CorreoClienteBase):
    id_correo: int
    id_cliente: int
    
    class Config:
        from_attributes = True

class ClienteBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    ci: Optional[str] = None
    nit: Optional[str] = None
    activo: bool = True

class ClienteCrear(ClienteBase):
    id_tenant: int

class ClienteRespuesta(ClienteBase):
    id_cliente: int
    id_tenant: int
    
    class Config:
        from_attributes = True
