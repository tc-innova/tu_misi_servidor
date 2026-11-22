from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class TipoProveedor(Base):
    __tablename__ = "tipo_proveedores"
    
    id_tipo_proveedor = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tenant = Column(BigInteger, ForeignKey("tenants.id_tenant"), nullable=False)
    nombre = Column(String(100), nullable=False)
    
    tenant = relationship("Tenant")

class Proveedor(Base):
    __tablename__ = "proveedores"
    
    id_proveedor = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tenant = Column(BigInteger, ForeignKey("tenants.id_tenant"), nullable=False)
    id_tipo_proveedor = Column(BigInteger, ForeignKey("tipo_proveedores.id_tipo_proveedor"), nullable=False)
    nombre = Column(String(150), nullable=False)
    
    tenant = relationship("Tenant")
    tipo_proveedor = relationship("TipoProveedor")
    celulares = relationship("CelularProveedor", back_populates="proveedor")
    correos = relationship("CorreoProveedor", back_populates="proveedor")

class CelularProveedor(Base):
    __tablename__ = "celulares_proveedores"
    
    id_proveedor = Column(BigInteger, ForeignKey("proveedores.id_proveedor"), primary_key=True)
    codigo_pais = Column(String(5), primary_key=True)
    numero = Column(String(15), primary_key=True)
    
    proveedor = relationship("Proveedor", back_populates="celulares")

class CorreoProveedor(Base):
    __tablename__ = "correos_proveedores"
    
    id_proveedor = Column(BigInteger, ForeignKey("proveedores.id_proveedor"), primary_key=True)
    correo = Column(String(150), primary_key=True)
    
    proveedor = relationship("Proveedor", back_populates="correos")
