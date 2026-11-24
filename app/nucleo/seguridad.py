from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import uuid
from app.nucleo.configuracion import configuracion

contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasenia(contrasenia_plana: str, contrasenia_hash: str) -> bool:
    return contexto_pwd.verify(contrasenia_plana, contrasenia_hash)

def obtener_hash_contrasenia(contrasenia: str) -> str:
    return contexto_pwd.hash(contrasenia)

def crear_token_acceso(id_usuario: int, tenants: list[dict]) -> str:
    expira = datetime.utcnow() + timedelta(minutes=configuracion.access_token_expire_minutes)
    payload = {
        "id_usuario": id_usuario,
        "tenants": tenants,
        "tipo": "acceso",
        "jti": str(uuid.uuid4()),
        "exp": expira
    }
    return jwt.encode(payload, configuracion.secret_key, algorithm=configuracion.algorithm)

def crear_token_refresco(id_usuario: int) -> str:
    expira = datetime.utcnow() + timedelta(days=7)
    payload = {
        "id_usuario": id_usuario,
        "tipo": "refresco",
        "jti": str(uuid.uuid4()),
        "exp": expira
    }
    return jwt.encode(payload, configuracion.secret_key, algorithm=configuracion.algorithm)

def verificar_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, configuracion.secret_key, algorithms=[configuracion.algorithm])
        return payload
    except JWTError:
        return None

