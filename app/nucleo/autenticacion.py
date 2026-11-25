from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.seguridad import verificar_token
from app.nucleo.base_datos import obtener_db

seguridad = HTTPBearer()

async def obtener_administrador_actual(
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
    
    if payload.get("tipo") != "acceso":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )
    
    if not payload.get("es_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requiere ser administrador"
        )
    
    id_administrador = payload.get("id_administrador")
    
    if not id_administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token incompleto"
        )
    
    query = text("""
        SELECT activo
        FROM administradores
        WHERE id_administrador = :id_administrador
    """)
    
    resultado = await db.execute(query, {"id_administrador": id_administrador})
    administrador = resultado.mappings().first()
    
    if not administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrador no encontrado"
        )
    
    if not administrador["activo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrador inactivo"
        )
    
    return {
        "id_administrador": id_administrador
    }

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
    
    if payload.get("tipo") != "acceso":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )
    
    id_usuario = payload.get("id_usuario")
    tenants = payload.get("tenants", [])
    
    if not id_usuario or not tenants:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token incompleto"
        )
    
    query = text("""
        SELECT activo
        FROM usuarios
        WHERE id_usuario = :id_usuario
    """)
    
    resultado = await db.execute(query, {"id_usuario": id_usuario})
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
    
    return {
        "id_usuario": id_usuario,
        "tenants": tenants
    }

async def obtener_usuario_temporal(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad)
):
    token = credenciales.credentials
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    if payload.get("tipo") != "temporal":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere token temporal"
        )
    
    id_usuario = payload.get("id_usuario")
    
    if not id_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token incompleto"
        )
    
    return {"id_usuario": id_usuario}
