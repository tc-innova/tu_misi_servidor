from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tenant = Column(BigInteger, ForeignKey("tenants.id_tenant"), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    ci = Column(String(20))
    nit = Column(String(20))
    
    tenant = relationship("Tenant")
    celulares = relationship("CelularCliente", back_populates="cliente")
    correos = relationship("CorreoCliente", back_populates="cliente")

class CelularCliente(Base):
    __tablename__ = "celulares_clientes"
    
    id_cliente = Column(BigInteger, ForeignKey("clientes.id_cliente"), primary_key=True)
    codigo_pais = Column(String(5), primary_key=True)
    numero = Column(String(15), primary_key=True)
    
    cliente = relationship("Cliente", back_populates="celulares")

class CorreoCliente(Base):
    __tablename__ = "correos_clientes"
    
    id_cliente = Column(BigInteger, ForeignKey("clientes.id_cliente"), primary_key=True)
    correo = Column(String(150), primary_key=True)
    
    cliente = relationship("Cliente", back_populates="correos")
