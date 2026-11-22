from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class CelularUsuario(Base):
    __tablename__ = "celulares_usuarios"
    
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id_usuario"), primary_key=True)
    codigo_pais = Column(String(5), primary_key=True)
    numero = Column(String(15), primary_key=True)
    
    usuario = relationship("Usuario", back_populates="celulares")
