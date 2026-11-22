from pydantic import BaseModel

class TenantBase(BaseModel):
    nombre: str

class TenantCrear(TenantBase):
    pass

class TenantRespuesta(TenantBase):
    id_tenant: int
    
    class Config:
        from_attributes = True
