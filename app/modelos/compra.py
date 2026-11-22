from sqlalchemy import Column, BigInteger, Date, Time, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class Compra(Base):
    __tablename__ = "compras"
    
    id_compra = Column(BigInteger, primary_key=True, autoincrement=True)
    id_proveedor = Column(BigInteger, ForeignKey("proveedores.id_proveedor"))
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_compra = Column(Date, nullable=False)
    hora_compra = Column(Time, nullable=False)
    
    proveedor = relationship("Proveedor")
    usuario = relationship("Usuario")
    detalles = relationship("DetalleCompra", back_populates="compra")

class DetalleCompra(Base):
    __tablename__ = "detalle_compras"
    
    id_compra = Column(BigInteger, ForeignKey("compras.id_compra"), primary_key=True)
    id_producto = Column(BigInteger, ForeignKey("productos.id_producto"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto")
