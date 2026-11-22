from sqlalchemy import Column, BigInteger, String
from app.nucleo.base_datos import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id_tenant = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True)
