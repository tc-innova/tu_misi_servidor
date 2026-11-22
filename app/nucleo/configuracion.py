from pydantic_settings import BaseSettings
from typing import List

class Configuracion(BaseSettings):
    entorno: str
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    db_pool_size: int
    db_max_overflow: int
    db_pool_timeout: int
    db_pool_recycle: int
    
    cors_origins: str
    cors_allow_credentials: bool
    cors_allow_methods: str
    cors_allow_headers: str
    
    @property
    def es_desarrollo(self) -> bool:
        return self.entorno.lower() == "desarrollo"
    
    @property
    def es_produccion(self) -> bool:
        return self.entorno.lower() == "produccion"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

configuracion = Configuracion()
