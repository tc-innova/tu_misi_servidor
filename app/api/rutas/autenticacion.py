from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.nucleo.base_datos import obtener_db
from app.nucleo.seguridad import verificar_contrasenia, crear_token_acceso
from app.nucleo.configuracion import configuracion
from app.nucleo.excepciones import ExcepcionNoAutorizado
from app.nucleo.limitador import limiter
from app.esquemas.usuario import UsuarioLogin, Token
from app.servicios.usuario import ServicioUsuario

router = APIRouter()

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def iniciar_sesion(request: Request, credenciales: UsuarioLogin, db: AsyncSession = Depends(obtener_db)):
    servicio = ServicioUsuario(db)
    usuario = await servicio.obtener_por_nombre_usuario(credenciales.usuario)
    
    if not usuario or not verificar_contrasenia(credenciales.contrasenia, usuario.contrasenia):
        raise ExcepcionNoAutorizado("Usuario o contraseña incorrectos")
    
    expira_acceso = timedelta(minutes=configuracion.access_token_expire_minutes)
    token_acceso = crear_token_acceso(
        data={"sub": usuario.usuario, "id_usuario": usuario.id_usuario, "id_tenant": usuario.id_tenant},
        expira_delta=expira_acceso
    )
    
    return {"access_token": token_acceso, "token_type": "bearer"}
