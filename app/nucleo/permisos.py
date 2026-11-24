from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.nucleo.autenticacion import obtener_usuario_actual, obtener_roles_usuario
from app.nucleo.base_datos import obtener_db

def requiere_roles(*roles_permitidos: str):
    async def validar_roles(
        usuario = Depends(obtener_usuario_actual),
        db: AsyncSession = Depends(obtener_db)
    ):
        roles_usuario = await obtener_roles_usuario(
            usuario["id_usuario"], 
            usuario["id_tenant"], 
            db
        )
        
        tiene_permiso = any(rol in roles_usuario for rol in roles_permitidos)
        
        if not tiene_permiso:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requiere uno de estos roles: {', '.join(roles_permitidos)}"
            )
        
        return usuario
    
    return validar_roles
