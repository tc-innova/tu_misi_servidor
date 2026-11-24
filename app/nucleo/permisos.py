from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.nucleo.autenticacion import obtener_usuario_actual
from app.nucleo.base_datos import obtener_db

def requiere_roles(*roles_permitidos: str):
    async def validar_roles(
        usuario = Depends(obtener_usuario_actual),
        db: AsyncSession = Depends(obtener_db)
    ):
        tenants = usuario.get("tenants", [])
        
        tiene_permiso = False
        for tenant in tenants:
            roles_tenant = tenant.get("roles", [])
            if any(rol in roles_tenant for rol in roles_permitidos):
                tiene_permiso = True
                break
        
        if not tiene_permiso:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requiere uno de estos roles: {', '.join(roles_permitidos)}"
            )
        
        return usuario
    
    return validar_roles
