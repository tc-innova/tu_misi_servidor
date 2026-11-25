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
    async def crear(self, usuario):
        query_rol = text("""
            SELECT nombre FROM roles WHERE id_rol = :id_rol
        """)
        resultado_rol = await self.db.execute(query_rol, {"id_rol": usuario.id_rol})
        rol = resultado_rol.mappings().first()
        
        if not rol:
            raise ExcepcionNoEncontrado("Rol")
        
        if rol["nombre"] == "administrador":
            from app.nucleo.excepciones import ExcepcionNoAutorizado
            raise ExcepcionNoAutorizado("No se puede asignar rol de administrador")
        
        query_tenant = text("""
            INSERT INTO tenants (nombre)
            VALUES (:nombre)
            RETURNING id_tenant
        """)
        resultado_tenant = await self.db.execute(query_tenant, {"nombre": usuario.nombre_negocio})
        id_tenant = resultado_tenant.scalar()
        
        contrasenia_hash = obtener_hash_contrasenia(usuario.contrasenia)
        
        query_usuario = text("""
            INSERT INTO usuarios (nombres, apellido_paterno, apellido_materno, 
                                 fecha_nacimiento, sexo, ci, usuario, contrasenia, activo)
            VALUES (:nombres, :apellido_paterno, :apellido_materno,
                    :fecha_nacimiento, :sexo, :ci, :usuario, :contrasenia, :activo)
            RETURNING id_usuario
        """)
        
        resultado = await self.db.execute(query_usuario, {
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
        
        query_relacion = text("""
            INSERT INTO usuarios_tenants (id_usuario, id_tenant, activo)
            VALUES (:id_usuario, :id_tenant, :activo)
        """)
        await self.db.execute(query_relacion, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant,
            "activo": True
        })
        
        query_rol_insert = text("""
            INSERT INTO usuarios_roles (id_usuario, id_tenant, id_rol)
            VALUES (:id_usuario, :id_tenant, :id_rol)
        """)
        await self.db.execute(query_rol_insert, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant,
            "id_rol": usuario.id_rol
        })
        
        await self.db.commit()
        return await self.obtener_por_id(id_usuario)
    
    @manejar_integridad("Usuario", "CI o usuario")
    @auditar("usuarios", "actualizar")
    async def actualizar(self, id_usuario: int, datos: dict):
        campos = []
        valores = {"id_usuario": id_usuario}
        
        if "nombres" in datos:
            campos.append("nombres = :nombres")
            valores["nombres"] = datos["nombres"]
        
        if "apellido_paterno" in datos:
            campos.append("apellido_paterno = :apellido_paterno")
            valores["apellido_paterno"] = datos["apellido_paterno"]
        
        if "apellido_materno" in datos:
            campos.append("apellido_materno = :apellido_materno")
            valores["apellido_materno"] = datos["apellido_materno"]
        
        if "fecha_nacimiento" in datos:
            campos.append("fecha_nacimiento = :fecha_nacimiento")
            valores["fecha_nacimiento"] = datos["fecha_nacimiento"]
        
        if "sexo" in datos:
            campos.append("sexo = :sexo")
            valores["sexo"] = datos["sexo"]
        
        if "ci" in datos:
            campos.append("ci = :ci")
            valores["ci"] = datos["ci"]
        
        if "activo" in datos:
            campos.append("activo = :activo")
            valores["activo"] = datos["activo"]
        
        if not campos:
            return await self.obtener_por_id(id_usuario)
        
        query = text(f"""
            UPDATE usuarios
            SET {", ".join(campos)}
            WHERE id_usuario = :id_usuario
            RETURNING id_usuario
        """)
        
        resultado = await self.db.execute(query, valores)
        if not resultado.scalar():
            raise ExcepcionNoEncontrado("Usuario")
        
        await self.db.commit()
        return await self.obtener_por_id(id_usuario)
    
    async def crear_con_tenant(self, usuario_data, nombre_negocio: str):
        return await self._crear_usuario_con_tenant(usuario_data, nombre_negocio, "propietario")
    
    async def crear_admin_con_tenant(self, usuario_data, nombre_negocio: str):
        contrasenia_hash = obtener_hash_contrasenia(usuario_data.contrasenia)
        
        query_admin = text("""
            INSERT INTO administradores (nombres, apellido_paterno, apellido_materno, 
                                        fecha_nacimiento, sexo, ci, usuario, contrasenia, activo)
            VALUES (:nombres, :apellido_paterno, :apellido_materno,
                    :fecha_nacimiento, :sexo, :ci, :usuario, :contrasenia, :activo)
            RETURNING id_administrador
        """)
        
        resultado = await self.db.execute(query_admin, {
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
        id_administrador = resultado.scalar()
        
        await self.db.commit()
        
        return {
            "id_usuario": id_administrador,
            "nombres": usuario_data.nombres,
            "apellido_paterno": usuario_data.apellido_paterno,
            "apellido_materno": usuario_data.apellido_materno,
            "fecha_nacimiento": usuario_data.fecha_nacimiento,
            "sexo": usuario_data.sexo,
            "ci": usuario_data.ci,
            "usuario": usuario_data.usuario,
            "activo": usuario_data.activo
        }
    
    async def _crear_usuario_con_tenant(self, usuario_data, nombre_negocio: str, nombre_rol: str):
        query_tenant = text("""
            INSERT INTO tenants (nombre)
            VALUES (:nombre)
            RETURNING id_tenant
        """)
        resultado_tenant = await self.db.execute(query_tenant, {"nombre": nombre_negocio})
        id_tenant = resultado_tenant.scalar()
        
        contrasenia_hash = obtener_hash_contrasenia(usuario_data.contrasenia)
        
        query_usuario = text("""
            INSERT INTO usuarios (nombres, apellido_paterno, apellido_materno, 
                                 fecha_nacimiento, sexo, ci, usuario, contrasenia, activo)
            VALUES (:nombres, :apellido_paterno, :apellido_materno,
                    :fecha_nacimiento, :sexo, :ci, :usuario, :contrasenia, :activo)
            RETURNING id_usuario
        """)
        
        resultado = await self.db.execute(query_usuario, {
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
        
        query_relacion = text("""
            INSERT INTO usuarios_tenants (id_usuario, id_tenant, activo)
            VALUES (:id_usuario, :id_tenant, :activo)
        """)
        await self.db.execute(query_relacion, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant,
            "activo": True
        })
        
        id_rol = await self.obtener_id_rol_por_nombre(nombre_rol)
        query_rol = text("""
            INSERT INTO usuarios_roles (id_usuario, id_tenant, id_rol)
            VALUES (:id_usuario, :id_tenant, :id_rol)
        """)
        await self.db.execute(query_rol, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant,
            "id_rol": id_rol
        })
        
        await self.db.commit()
        
        return {
            "id_usuario": id_usuario,
            "nombres": usuario_data.nombres,
            "apellido_paterno": usuario_data.apellido_paterno,
            "apellido_materno": usuario_data.apellido_materno,
            "fecha_nacimiento": usuario_data.fecha_nacimiento,
            "sexo": usuario_data.sexo,
            "ci": usuario_data.ci,
            "usuario": usuario_data.usuario,
            "activo": usuario_data.activo
        }
    
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
            RETURNING id_usuario, codigo_pais, numero
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
            RETURNING id_usuario, correo
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "correo": correo.correo
        })
        await self.db.commit()
        return resultado.mappings().first()
    
    async def eliminar_celular(self, id_usuario: int, codigo_pais: str, numero: str):
        query = text("""
            DELETE FROM celulares_usuarios 
            WHERE id_usuario = :id_usuario AND codigo_pais = :codigo_pais AND numero = :numero
            RETURNING id_usuario
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "codigo_pais": codigo_pais,
            "numero": numero
        })
        if not resultado.first():
            raise ExcepcionNoEncontrado("Celular")
        await self.db.commit()
    
    async def eliminar_correo(self, id_usuario: int, correo: str):
        query = text("""
            DELETE FROM correos_usuarios 
            WHERE id_usuario = :id_usuario AND correo = :correo
            RETURNING id_usuario
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "correo": correo
        })
        if not resultado.first():
            raise ExcepcionNoEncontrado("Correo")
        await self.db.commit()
    
    async def listar_celulares(self, id_usuario: int):
        query = text("""
            SELECT id_usuario, codigo_pais, numero
            FROM celulares_usuarios
            WHERE id_usuario = :id_usuario
        """)
        resultado = await self.db.execute(query, {"id_usuario": id_usuario})
        return resultado.mappings().all()
    
    async def listar_correos(self, id_usuario: int):
        query = text("""
            SELECT id_usuario, correo
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
            SELECT id_usuario, nombres, apellido_paterno, apellido_materno,
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
            SELECT id_usuario, nombres, apellido_paterno, apellido_materno,
                   fecha_nacimiento, sexo, ci, usuario, contrasenia, activo
            FROM usuarios
            WHERE usuario = :usuario
        """)
        resultado = await self.db.execute(query, {"usuario": nombre_usuario})
        return resultado.mappings().first()
    
    async def listar_por_tenant(self, id_tenant: int, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT DISTINCT u.id_usuario, u.nombres, u.apellido_paterno, u.apellido_materno,
                   u.fecha_nacimiento, u.sexo, u.ci, u.usuario, u.activo
            FROM usuarios u
            INNER JOIN usuarios_tenants ut ON u.id_usuario = ut.id_usuario
            WHERE ut.id_tenant = :id_tenant AND ut.activo = TRUE
            ORDER BY u.id_usuario
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "id_tenant": id_tenant,
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()
    
    async def listar_todos(self, skip: int = 0, limit: int = 100):
        query = text("""
            SELECT DISTINCT u.id_usuario, u.nombres, u.apellido_paterno, u.apellido_materno,
                   u.fecha_nacimiento, u.sexo, u.ci, u.usuario, u.activo
            FROM usuarios u
            INNER JOIN usuarios_roles ur ON u.id_usuario = ur.id_usuario
            INNER JOIN roles r ON ur.id_rol = r.id_rol
            WHERE r.nombre = 'propietario'
            ORDER BY u.id_usuario
            OFFSET :skip LIMIT :limit
        """)
        resultado = await self.db.execute(query, {
            "skip": skip,
            "limit": limit
        })
        return resultado.mappings().all()

    async def listar_roles_disponibles(self):
        query = text("""
            SELECT id_rol, nombre
            FROM roles
            WHERE nombre != 'administrador'
            ORDER BY nombre
        """)
        resultado = await self.db.execute(query)
        return resultado.mappings().all()
    
    async def asignar_rol(self, id_usuario: int, id_tenant: int, id_rol: int):
        query_rol = text("""
            SELECT nombre FROM roles WHERE id_rol = :id_rol
        """)
        resultado_rol = await self.db.execute(query_rol, {"id_rol": id_rol})
        rol = resultado_rol.mappings().first()
        
        if not rol:
            raise ExcepcionNoEncontrado("Rol")
        
        if rol["nombre"] == "administrador":
            from app.nucleo.excepciones import ExcepcionNoAutorizado
            raise ExcepcionNoAutorizado("No se puede asignar rol de administrador")
        
        query_verificar = text("""
            SELECT 1 FROM usuarios WHERE id_usuario = :id_usuario
        """)
        resultado = await self.db.execute(query_verificar, {"id_usuario": id_usuario})
        if not resultado.scalar():
            raise ExcepcionNoEncontrado("Usuario")
        
        query_insert = text("""
            INSERT INTO usuarios_roles (id_usuario, id_tenant, id_rol)
            VALUES (:id_usuario, :id_tenant, :id_rol)
            ON CONFLICT (id_usuario, id_tenant, id_rol) DO NOTHING
        """)
        await self.db.execute(query_insert, {
            "id_usuario": id_usuario,
            "id_tenant": id_tenant,
            "id_rol": id_rol
        })
        await self.db.commit()
        
        return {"mensaje": "Rol asignado correctamente"}
    
    async def remover_rol(self, id_usuario: int, id_rol: int):
        query = text("""
            DELETE FROM usuarios_roles
            WHERE id_usuario = :id_usuario AND id_rol = :id_rol
            RETURNING id_usuario
        """)
        resultado = await self.db.execute(query, {
            "id_usuario": id_usuario,
            "id_rol": id_rol
        })
        if not resultado.scalar():
            raise ExcepcionNoEncontrado("Rol de usuario")
        
        await self.db.commit()
