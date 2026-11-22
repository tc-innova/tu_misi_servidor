from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.nucleo.seguridad import obtener_hash_contrasenia
from app.nucleo.excepciones import ExcepcionNoEncontrado
from app.nucleo.manejadores import manejar_integridad
from app.nucleo.auditoria import auditar

class ServicioUsuario:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @manejar_integridad("Usuario", "CI o usuario")
    @auditar("usuarios", "crear")
    async def crear(self, usuario, id_rol: int = None):
        contrasenia_hash = obtener_hash_contrasenia(usuario.contrasenia)
        
        query_usuario = text("""
            INSERT INTO usuarios (id_tenant, nombres, apellido_paterno, apellido_materno, 
                                 fecha_nacimiento, sexo, ci, usuario, contrasenia, activo)
            VALUES (:id_tenant, :nombres, :apellido_paterno, :apellido_materno,
                    :fecha_nacimiento, :sexo, :ci, :usuario, :contrasenia, :activo)
            RETURNING id_usuario
        """)
        
        resultado = await self.db.execute(query_usuario, {
            "id_tenant": usuario.id_tenant,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "fecha_nacimiento": usuario.fecha_nacimiento,
            "sexo": usuario.sexo,
            "ci": usuario.ci,
            "usuario": usuario.usuario,
            "contrasenia": contrasenia_hash,
            "activo": usuario.activo
        })
        id_usuario = resultado.scalar()
        
        if id_rol:
            query_rol = text("""
                INSERT INTO usuarios_roles (id_usuario, id_rol)
                VALUES (:id_usuario, :id_rol)
            """)
            await self.db.execute(query_rol, {
                "id_usuario": id_usuario,
                "id_rol": id_rol
            })
        
        await self.db.commit()
        return await self.obtener_por_id(id_usuario)
    
    @manejar_integridad("Usuario cliente prueba", "CI o usuario")
    @auditar("usuarios", "crear_con_tenant")
    async def crear_con_tenant(self, usuario_data, nombre_negocio: str):
        query_tenant = text("""
            INSERT INTO tenants (nombre)
            VALUES (:nombre)
            RETURNING id_tenant
        """)
        resultado_tenant = await self.db.execute(query_tenant, {"nombre": nombre_negocio})
        id_tenant = resultado_tenant.scalar()
        
        contrasenia_hash = obtener_hash_contrasenia(usuario_data.contrasenia)
        
        query_usuario = text("""
            INSERT INTO usuarios (id_tenant, nombres, apellido_paterno, apellido_materno, 
                                 fecha_nacimiento, sexo, ci, usuario, contrasenia, activo)
            VALUES (:id_tenant, :nombres, :apellido_paterno, :apellido_materno,
                    :fecha_nacimiento, :sexo, :ci, :usuario, :contrasenia, :activo)
            RETURNING id_usuario
        """)
        
        resultado = await self.db.execute(query_usuario, {
            "id_tenant": id_tenant,
            "nombres": usuario_data.nombres,
            "apellido_paterno": usuario_data.apellido_paterno,
            "apellido_materno": usuario_data.apellido_materno,
            "fecha_nacimiento": usuario_data.fecha_nacimiento,
            "sexo": usuario_data.sexo,
            "ci": usuario_data.ci,
            "usuario": usuario_data.usuario,
            "contrasenia": contrasenia_hash,
            "activo": usuario_data.activo
        })
        id_usuario = resultado.scalar()
        
        id_rol_cliente = await self.obtener_id_rol_por_nombre("cliente")
        query_rol = text("""
            INSERT INTO usuarios_roles (id_usuario, id_rol)
            VALUES (:id_usuario, :id_rol)
        """)
        await self.db.execute(query_rol, {
            "id_usuario": id_usuario,
            "id_rol": id_rol_cliente
        })
        
        await self.db.commit()
        return await self.obtener_por_id(id_usuario)
    
    @manejar_integridad("Celular", "número")
    @auditar("celulares_usuarios", "crear")
    async def agregar_celular(self, id_usuario: int, celular):
        query_verificar = text("SELECT 1 FROM usuarios WHERE id_usuario = :id_usuario")
        resultado = await self.db.execute(query_verificar, {"id_usuario": id_usuario})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Usuario")
        
        query = text("""
            INSERT INTO celulares_usuarios (id_usuario, codigo_pais, numero)
            VALUES (:id_usuario, :codigo_pais, :numero)
            RETURNING id_celular, id_usuario, codigo_pais, numero
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "codigo_pais": celular.codigo_pais,
            "numero": celular.numero
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    @manejar_integridad("Correo", "correo")
    @auditar("correos_usuarios", "crear")
    async def agregar_correo(self, id_usuario: int, correo):
        query_verificar = text("SELECT 1 FROM usuarios WHERE id_usuario = :id_usuario")
        resultado = await self.db.execute(query_verificar, {"id_usuario": id_usuario})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Usuario")
        
        query = text("""
            INSERT INTO correos_usuarios (id_usuario, correo)
            VALUES (:id_usuario, :correo)
            RETURNING id_correo, id_usuario, correo
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "correo": correo.correo
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def eliminar_celular(self, id_celular: int):
        query = text("DELETE FROM celulares_usuarios WHERE id_celular = :id_celular RETURNING id_celular")
        resultado = await self.db.execute(query, {"id_celular": id_celular})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Celular")
        await self.db.commit()
    
    async def eliminar_correo(self, id_correo: int):
        query = text("DELETE FROM correos_usuarios WHERE id_correo = :id_correo RETURNING id_correo")
        resultado = await self.db.execute(query, {"id_correo": id_correo})
        if not resultado.first():
            raise ExcepcionNoEncontrado("Correo")
        await self.db.commit()
    
    async def listar_celulares(self, id_usuario: int):
        query = text("""
            SELECT id_celular, id_usuario, codigo_pais, numero
            FROM celulares_usuarios
            WHERE id_usuario = :id_usuario
        """)
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        return resultado.mappings().all()
    
    async def listar_correos(self, id_usuario: int):
        query = text("""
            SELECT id_correo, id_usuario, correo
            FROM correos_usuarios
            WHERE id_usuario = :id_usuario
        """)
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        return resultado.mappings().all()
    
    async def obtener_id_rol_por_nombre(self, nombre_rol: str):
        query = text("SELECT id_rol FROM roles WHERE nombre = :nombre")
        resultado = await self.db.execute(query, {"nombre": nombre_rol})
        rol = resultado.mappings().first()
        if not rol:
            raise ExcepcionNoEncontrado("Rol")
        return rol["id_rol"]
    
    async def obtener_por_id(self, id_usuario: int):
        query = text("""
            SELECT id_usuario, id_tenant, nombres, apellido_paterno, apellido_materno,
                   fecha_nacimiento, sexo, ci, usuario, activo
            FROM usuarios
            WHERE id_usuario = :id_usuario
        """)
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        usuario = resultado.mappings().first()
        if not usuario:
            raise ExcepcionNoEncontrado("Usuario")
        return usuario
    
    async def obtener_por_nombre_usuario(self, nombre_usuario: str):
        query = text("""
            SELECT id_usuario, id_tenant, nombres, apellido_paterno, apellido_materno,
                   fecha_nacimiento, sexo, ci, usuario, contrasenia, activo
            FROM usuarios
            WHERE usuario = :usuario
        """)
        resultado = await self.db.execute(query, {"usuario": nombre_usuario})
        return resultado.mappings().first()
    
    async def listar_por_tenant(self, id_tenant: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT id_usuario, id_tenant, nombres, apellido_paterno, apellido_materno,
                   fecha_nacimiento, sexo, ci, usuario, activo
            FROM usuarios
            WHERE id_tenant = :id_tenant
            ORDER BY id_usuario
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": id_tenant,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
