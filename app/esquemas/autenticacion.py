from pydantic import BaseModel
from typing import List

class LoginCredenciales(BaseModel):
    usuario: str
    contrasenia: str

class TokenTemporal(BaseModel):
    token_temporal: str
    tipo_token: str

class TenantDisponible(BaseModel):
    id_tenant: int
    nombre: str
    activo: bool

class SeleccionTenant(BaseModel):
    id_tenant: int

class TokenAcceso(BaseModel):
    token_acceso: str
    token_refresco: str
    tipo_token: str
    id_tenant: int
    roles: List[str]

class TokenRefrescado(BaseModel):
    token_acceso: str
    tipo_token: str
    roles: List[str]
