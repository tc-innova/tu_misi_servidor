from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.seguridad import verificar_token
from app.nucleo.base_datos import obtener_db

seguridad = HTTPBearer()

async def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad),
    db: AsyncSession = Depends(obtener_db)
):
    token = credenciales.credentials
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    query = text("""
        SELECT id_usuario, id_tenant, usuario, activo
        FROM usuarios
        WHERE id_usuario = :id_usuario
    """)
    
    resultado = await db.execute(query, {"id_usuario": payload.get("id_usuario")})
    usuario = resultado.mappings().first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not usuario["activo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return usuario

async def obtener_roles_usuario(id_usuario: int, db: AsyncSession):
    query = text("""
        SELECT r.nombre
        FROM roles r
        INNER JOIN usuarios_roles ur ON r.id_rol = ur.id_rol
        WHERE ur.id_usuario = :id_usuario
    """)
    
    resultado = await db.execute(query, {"id_usuario": id_usuario})
    return [row["nombre"] for row in resultado.mappings().all()]
