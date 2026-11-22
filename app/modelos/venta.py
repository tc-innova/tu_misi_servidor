from sqlalchemy import Column, BigInteger, String, Date, Time, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from app.nucleo.base_datos import Base

class EstadoVenta(Base):
    __tablename__ = "estados_venta"
    
    id_estado_venta = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False, unique=True)

class Venta(Base):
    __tablename__ = "ventas"
    
    id_venta = Column(BigInteger, primary_key=True, autoincrement=True)
    id_cliente = Column(BigInteger, ForeignKey("clientes.id_cliente"))
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_estado_venta = Column(BigInteger, ForeignKey("estados_venta.id_estado_venta"), nullable=False)
    fecha_venta = Column(Date, nullable=False)
    hora_venta = Column(Time, nullable=False)
    
    cliente = relationship("Cliente")
    usuario = relationship("Usuario")
    estado_venta = relationship("EstadoVenta")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"
    
    id_venta = Column(BigInteger, ForeignKey("ventas.id_venta"), primary_key=True)
    id_producto = Column(BigInteger, ForeignKey("productos.id_producto"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")
