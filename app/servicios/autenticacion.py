from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.seguridad import verificar_contrasenia, crear_token_acceso, crear_token_refresco
from app.nucleo.excepciones import ExcepcionNoAutorizado

class ServicioAutenticacion:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def login_admin(self, usuario: str, contrasenia: str) -> dict:
        query = text("""
            SELECT id_administrador, contrasenia, activo
            FROM administradores
            WHERE usuario = :usuario
        """)
        
        resultado = await self.db.execute(query, {"usuario": usuario})
        admin_bd = resultado.mappings().first()
        
        if not admin_bd:
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        if not admin_bd["activo"]:
            raise ExcepcionNoAutorizado("Administrador inactivo")
        
        if not verificar_contrasenia(contrasenia, admin_bd["contrasenia"]):
            raise ExcepcionNoAutorizado("Credenciales inválidas")
        
        token_acceso = crear_token_acceso(admin_bd["id_administrador"], es_admin=True)
        
        return {
            "token_acceso": token_acceso,
            "tipo_token": "acceso"
        }
    
    async def login_usuario(self, usuario: str, contrasenia: str) -> dict:
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
        
        tenants = await self.obtener_tenants_con_roles(usuario_bd["id_usuario"])
        
        if not tenants:
            raise ExcepcionNoAutorizado("No tienes acceso a ningún negocio")
        
        tiene_rol_admin = any(
            "administrador" in tenant.get("roles", []) 
            for tenant in tenants
        )
        
        if tiene_rol_admin:
            raise ExcepcionNoAutorizado("Esta ruta es solo para clientes")
        
        token_acceso = crear_token_acceso(usuario_bd["id_usuario"], tenants)
        
        return {
            "token_acceso": token_acceso,
            "tipo_token": "acceso"
        }
    
    async def obtener_tenants_con_roles(self, id_usuario: int) -> list[dict]:
        query = text("""
            SELECT DISTINCT ut.id_tenant, t.nombre, r.nombre as rol
            FROM usuarios_tenants ut
            INNER JOIN tenants t ON ut.id_tenant = t.id_tenant
            LEFT JOIN usuarios_roles ur ON ut.id_usuario = ur.id_usuario AND ut.id_tenant = ur.id_tenant
            LEFT JOIN roles r ON ur.id_rol = r.id_rol
            WHERE ut.id_usuario = :id_usuario AND ut.activo = TRUE
            ORDER BY t.nombre, r.nombre
        """)
        
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        filas = resultado.mappings().all()
        
        tenants_dict = {}
        for fila in filas:
            id_tenant = fila["id_tenant"]
            if id_tenant not in tenants_dict:
                tenants_dict[id_tenant] = {
                    "id_tenant": id_tenant,
                    "nombre": fila["nombre"],
                    "roles": []
                }
            if fila["rol"]:
                tenants_dict[id_tenant]["roles"].append(fila["rol"])
        
        return list(tenants_dict.values())
    
    async def refrescar_token(self, id_usuario: int) -> dict:
        query_verificar = text("""
            SELECT activo
            FROM usuarios
            WHERE id_usuario = :id_usuario
        """)
        
        resultado = await self.db.execute(query_verificar, {"id_usuario": id_usuario})
        usuario = resultado.mappings().first()
        
        if not usuario or not usuario["activo"]:
            raise ExcepcionNoAutorizado("Usuario inactivo")
        
        tenants = await self.obtener_tenants_con_roles(id_usuario)
        
        if not tenants:
            raise ExcepcionNoAutorizado("No tienes acceso a ningún negocio")
        
        token_acceso = crear_token_acceso(id_usuario, tenants)
        
        return {
            "token_acceso": token_acceso,
            "tipo_token": "acceso"
        }
