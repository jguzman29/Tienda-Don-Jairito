from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from datetime import datetime

USUARIO = "root"
PASSWORD = "Juanguzman2008"
DB = "tiendadb"
HOST = "localhost"
PORT = "3306"

DB_URL = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(DB_URL, pool_pre_ping=True, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Cliente(Base):
    __tablename__ = "clientes"
    cedula = Column(String(20), primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    
    ventas = relationship("Venta", back_populates="cliente")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Integer, nullable=False)

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cedula_cliente = Column(String(20), ForeignKey("clientes.cedula"), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Integer, nullable=False)

    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")

def inicializar_bd():
    try:
        with engine.connect() as con:
            con.execute(text("SELECT 1"))
        Base.metadata.create_all(engine)
        poblar_inventario_inicial()
        return True
    except OperationalError as e:
        print("Error al conectar a la base de datos:", e)
        return False

def poblar_inventario_inicial():
    session = SessionLocal()
    productos_defecto = [
        {"nombre": "Leche", "precio": 4000}, {"nombre": "Huevos", "precio": 1000},
        {"nombre": "Arroz", "precio": 2000}, {"nombre": "Pan", "precio": 1000},
        {"nombre": "Azucar", "precio": 3500}, {"nombre": "Carne", "precio": 14000},
        {"nombre": "Pollo", "precio": 12000}, {"nombre": "Harina", "precio": 3000},
        {"nombre": "Panela", "precio": 3500}, {"nombre": "Aceite", "precio": 9500},
        {"nombre": "Cafe", "precio": 6000}, {"nombre": "Sal", "precio": 1500},
        {"nombre": "Frijol", "precio": 4500}, {"nombre": "Lentejas", "precio": 4000},
        {"nombre": "Pasta", "precio": 2500}, {"nombre": "Mantequilla", "precio": 5000},
        {"nombre": "Chocolate", "precio": 4500}, {"nombre": "Atun", "precio": 6500},
        {"nombre": "Gaseosa", "precio": 3500}, {"nombre": "Jabon", "precio": 3000}
    ]

    for item in productos_defecto:
        existe = session.query(Producto).filter_by(nombre=item["nombre"]).first()
        if not existe:
            session.add(Producto(nombre=item["nombre"], precio=item["precio"]))
            
    session.commit()
    session.close()

