from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.seguridad import verificar_contrasenia, crear_token_temporal, crear_token_acceso, crear_token_refresco
from app.nucleo.excepciones import ExcepcionNoAutorizado
from app.nucleo.autenticacion import obtener_roles_usuario

class ServicioAutenticacion:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def login_credenciales(self, usuario: str, contrasenia: str) -> dict:
        query = text("""
            SELECT id_usuario, contrasenia, activo
            FROM usuarios
            WHERE usuario = :usuario
        """)
        
        resultado = await self.db.execute(query, {"usuario": usuario})
        usuario_bd = resultado.mappings().first()
        
        if not usuario_bd:
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        if not usuario_bd["activo"]:
            raise ExcepcionNoAutorizado("Usuario inactivo")
        
        if not verificar_contrasenia(contrasenia, usuario_bd["contrasenia"]):
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        token_temporal = crear_token_temporal(usuario_bd["id_usuario"])
        
        return {
            "token_temporal": token_temporal,
            "tipo_token": "temporal"
        }
    
    async def login_admin(self, usuario: str, contrasenia: str) -> dict:
        query = text("""
            SELECT u.id_usuario, u.contrasenia, u.activo
            FROM usuarios u
            WHERE u.usuario = :usuario
        """)
        
        resultado = await self.db.execute(query, {"usuario": usuario})
        usuario_bd = resultado.mappings().first()
        
        if not usuario_bd:
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        if not usuario_bd["activo"]:
            raise ExcepcionNoAutorizado("Usuario inactivo")
        
        if not verificar_contrasenia(contrasenia, usuario_bd["contrasenia"]):
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        query_admin = text("""
            SELECT ur.id_tenant, r.nombre
            FROM usuarios_roles ur
            INNER JOIN roles r ON ur.id_rol = r.id_rol
            WHERE ur.id_usuario = :id_usuario AND r.nombre = 'administrador'
            LIMIT 1
        """)
        
        resultado_rol = await self.db.execute(query_admin, {"id_usuario": usuario_bd["id_usuario"]})
        admin_rol = resultado_rol.mappings().first()
        
        if not admin_rol:
            raise ExcepcionNoAutorizado("No tienes permisos de administrador")
        
        id_tenant = admin_rol["id_tenant"]
        roles = ["administrador"]
        
        token_acceso = crear_token_acceso(usuario_bd["id_usuario"], id_tenant, roles)
        token_refresco = crear_token_refresco(usuario_bd["id_usuario"], id_tenant)
        
        return {
            "token_acceso": token_acceso,
            "token_refresco": token_refresco,
            "tipo_token": "acceso",
            "id_tenant": id_tenant,
            "roles": roles
        }
    
    async def listar_tenants_usuario(self, id_usuario: int) -> list[dict]:
        query = text("""
            SELECT t.id_tenant, t.nombre, ut.activo
            FROM tenants t
            INNER JOIN usuarios_tenants ut ON t.id_tenant = ut.id_tenant
            WHERE ut.id_usuario = :id_usuario AND ut.activo = TRUE
            ORDER BY t.nombre
        """)
        
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        return [dict(fila) for fila in resultado.mappings().all()]
    
    async def seleccionar_tenant(self, id_usuario: int, id_tenant: int) -> dict:
        query_verificar = text("""
            SELECT ut.activo, u.activo as usuario_activo
            FROM usuarios_tenants ut
            INNER JOIN usuarios u ON ut.id_usuario = u.id_usuario
            WHERE ut.id_usuario = :id_usuario AND ut.id_tenant = :id_tenant
        """)
        
        resultado = await self.db.execute(query_verificar, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant
        })
        relacion = resultado.mappings().first()
        
        if not relacion:
            raise ExcepcionNoAutorizado("No tienes acceso a este negocio")
        
        if not relacion["activo"] or not relacion["usuario_activo"]:
            raise ExcepcionNoAutorizado("Usuario inactivo en este negocio")
        
        roles = await obtener_roles_usuario(id_usuario, id_tenant, self.db)
        
        token_acceso = crear_token_acceso(id_usuario, id_tenant, roles)
        token_refresco = crear_token_refresco(id_usuario, id_tenant)
        
        return {
            "token_acceso": token_acceso,
            "token_refresco": token_refresco,
            "tipo_token": "acceso",
            "id_tenant": id_tenant,
            "roles": roles
        }
    
    async def refrescar_token(self, id_usuario: int, id_tenant: int) -> dict:
        query_verificar = text("""
            SELECT ut.activo, u.activo as usuario_activo
            FROM usuarios_tenants ut
            INNER JOIN usuarios u ON ut.id_usuario = u.id_usuario
            WHERE ut.id_usuario = :id_usuario AND ut.id_tenant = :id_tenant
        """)
        
        resultado = await self.db.execute(query_verificar, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant
        })
        relacion = resultado.mappings().first()
        
        if not relacion or not relacion["activo"] or not relacion["usuario_activo"]:
            raise ExcepcionNoAutorizado("Usuario inactivo en este negocio")
        
        roles = await obtener_roles_usuario(id_usuario, id_tenant, self.db)
        
        token_acceso = crear_token_acceso(id_usuario, id_tenant, roles)
        
        return {
            "token_acceso": token_acceso,
            "tipo_token": "acceso",
            "roles": roles
        }
