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
    
    if payload.get("tipo") != "acceso":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )
    
    id_usuario = payload.get("id_usuario")
    id_tenant = payload.get("id_tenant")
    
    if not id_usuario or not id_tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token incompleto"
        )
    
    query = text("""
        SELECT u.id_usuario, u.activo as usuario_activo, ut.activo as tenant_activo
        FROM usuarios u
        INNER JOIN usuarios_tenants ut ON u.id_usuario = ut.id_usuario
        WHERE u.id_usuario = :id_usuario AND ut.id_tenant = :id_tenant
    """)
    
    resultado = await db.execute(query, {"id_usuario": id_usuario, "id_tenant": id_tenant})
    usuario = resultado.mappings().first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado en este tenant"
        )
    
    if not usuario["usuario_activo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    if not usuario["tenant_activo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo en este negocio"
        )
    
    return {
        "id_usuario": id_usuario,
        "id_tenant": id_tenant,
        "roles": payload.get("roles", [])
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

async def obtener_roles_usuario(id_usuario: int, id_tenant: int, db: AsyncSession) -> list[str]:
    query = text("""
        SELECT r.nombre
        FROM roles r
        INNER JOIN usuarios_roles ur ON r.id_rol = ur.id_rol
        WHERE ur.id_usuario = :id_usuario AND ur.id_tenant = :id_tenant
    """)
    
    resultado = await db.execute(query, {"id_usuario": id_usuario, "id_tenant": id_tenant})
    return [row["nombre"] for row in resultado.mappings().all()]

