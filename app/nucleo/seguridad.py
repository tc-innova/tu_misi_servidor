from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.nucleo.configuracion import configuracion

contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasenia(contrasenia_plana: str, contrasenia_hash: str) -> bool:
    return contexto_pwd.verify(contrasenia_plana, contrasenia_hash)

def obtener_hash_contrasenia(contrasenia: str) -> str:
    return contexto_pwd.hash(contrasenia)

def crear_token_acceso(data: dict, expira_delta: Optional[timedelta] = None):
    a_codificar = data.copy()
    
    if not expira_delta:
        expira_delta = timedelta(minutes=15)
    
    expira = datetime.utcnow() + expira_delta
    a_codificar.update({"exp": expira})
    token_codificado = jwt.encode(a_codificar, configuracion.secret_key, algorithm=configuracion.algorithm)
    return token_codificado

def verificar_token(token: str):
    payload = jwt.decode(token, configuracion.secret_key, algorithms=[configuracion.algorithm])
    return payload
