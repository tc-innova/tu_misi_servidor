from sqlalchemy import Column, BigInteger, String, Numeric, Integer, ForeignKey, LargeBinary
from app.nucleo.base_datos import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id_producto = Column(BigInteger, primary_key=True, autoincrement=True)
    id_tipo_producto = Column(BigInteger, ForeignKey("tipo_productos.id_tipo_producto"), nullable=False)
    codigo = Column(String(50), nullable=False)
    nombre = Column(String(150), nullable=False)
    precio = Column(Numeric(12, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    cantidad_minima = Column(Integer, nullable=False)

class FotoProducto(Base):
    __tablename__ = "fotos_productos"
    
    id_producto = Column(BigInteger, ForeignKey("productos.id_producto"), primary_key=True)
    numero = Column(Integer, primary_key=True)
    foto = Column(LargeBinary, nullable=False)

