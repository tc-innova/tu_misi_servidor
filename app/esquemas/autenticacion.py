from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class LoginCredenciales(BaseModel):
    usuario: str
    contrasenia: str

class TenantInfo(BaseModel):
    id_tenant: Optional[int] = None
    nombre: Optional[str] = None
    roles: List[str]

class TokenAcceso(BaseModel):
    token_acceso: str
    token_refresco: str
    tipo_token: str
    tenants: Optional[List[TenantInfo]] = None

class TokenRefrescado(BaseModel):
    token_acceso: str
    tipo_token: str
    tenants: Optional[List[TenantInfo]] = None
