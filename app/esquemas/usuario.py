from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class RolBase(BaseModel):
    nombre: str

class RolRespuesta(RolBase):
    id_rol: int
    
    class Config:
        from_attributes = True

class CelularBase(BaseModel):
    codigo_pais: str
    numero: str

class CelularRespuesta(CelularBase):
    id_celular: int
    id_usuario: int
    
    class Config:
        from_attributes = True

class CorreoBase(BaseModel):
    correo: str

class CorreoRespuesta(CorreoBase):
    id_correo: int
    id_usuario: int
    
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    sexo: bool
    ci: str
    usuario: str
    activo: bool = True

class UsuarioCrear(UsuarioBase):
    nombre_negocio: str
    id_rol: int
    contrasenia: str

class UsuarioClientePruebaCrear(BaseModel):
    nombre_negocio: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    sexo: bool
    ci: str
    usuario: str
    contrasenia: str
    activo: bool = True

class UsuarioRespuesta(UsuarioBase):
    id_usuario: int
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    usuario: str
    contrasenia: str

class Token(BaseModel):
    access_token: str
    token_type: str


class CambiarContrasenia(BaseModel):
    contrasenia_actual: str
    contrasenia_nueva: str

class AsignarRol(BaseModel):
    id_tenant: int
    id_rol: int
