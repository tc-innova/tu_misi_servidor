from sqlalchemy import Column, BigInteger, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class Rol(Base):
    __tablename__ = "roles"
    
    id_rol = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tenant = Column(BigInteger, ForeignKey("tenants.id_tenant"), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Boolean, nullable=False)
    ci = Column(String(20), nullable=False)
    usuario = Column(String(50), nullable=False)
    contrasenia = Column(String(255), nullable=False)
    
    tenant = relationship("Tenant")
    celulares = relationship("CelularUsuario", back_populates="usuario")
    correos = relationship("CorreoUsuario", back_populates="usuario")

class UsuarioRol(Base):
    __tablename__ = "usuarios_roles"
    
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id_usuario"), primary_key=True)
    id_rol = Column(BigInteger, ForeignKey("roles.id_rol"), primary_key=True)
    
    usuario = relationship("Usuario")
    rol = relationship("Rol")
