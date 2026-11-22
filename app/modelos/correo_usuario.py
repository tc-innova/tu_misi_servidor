from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class CorreoUsuario(Base):
    __tablename__ = "correos_usuarios"
    
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id_usuario"), primary_key=True)
    correo = Column(String(150), primary_key=True)
    
    usuario = relationship("Usuario", back_populates="correos")
