from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class TipoProducto(Base):
    __tablename__ = "tipo_productos"

    id_tipo_producto = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tenant = Column(BigInteger, ForeignKey("tenants.id_tenant"), nullable=False)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    tenant = relationship("Tenant", back_populates="tipo_productos")
    productos = relationship("Producto", back_populates="tipo_producto")
