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
    if session.query(Producto).count() == 0:
        productos_defecto = [
        {"nombre": "Leche", "precio": 4000},
        {"nombre": "Huevos", "precio": 1000},
        {"nombre": "Arroz", "precio": 2000},
        {"nombre": "Pan", "precio": 1000},
        {"nombre": "Azucar", "precio": 3500},
        {"nombre": "Carne", "precio": 14000},
        {"nombre": "Pollo", "precio": 12000},
        {"nombre": "Harina", "precio": 3000},
        {"nombre": "Panela", "precio": 3500},
        {"nombre": "Aceite", "precio": 9500},
        {"nombre": "Cafe", "precio": 6000},
        {"nombre": "Sal", "precio": 1500},
        {"nombre": "Frijol", "precio": 4500},
        {"nombre": "Lentejas", "precio": 4000},
        {"nombre": "Pasta", "precio": 2500},
        {"nombre": "Mantequilla", "precio": 5000},
        {"nombre": "Chocolate", "precio": 4500},
        {"nombre": "Atun", "precio": 6500},
        {"nombre": "Gaseosa", "precio": 3500},
        {"nombre": "Jabon", "precio": 3000}
        ]
        for p in productos_defecto:
            session.add(Producto(nombre=p["nombre"], precio=p["precio"]))
        session.commit()
    session.close()




Inventario = [
    {"id": 1, "producto": "Leche", "precio": 4000},
    {"id": 2, "producto": "Huevos", "precio": 1000},
    {"id": 3, "producto": "Arroz", "precio": 2000},
    {"id": 4, "producto": "Pan", "precio": 1000},
    {"id": 5, "producto": "Azucar", "precio": 3500},
    {"id": 6, "producto": "Carne", "precio": 14000},
    {"id": 7, "producto": "Pollo", "precio": 12000},
    {"id": 8, "producto": "Harina", "precio": 3000},
    {"id": 9, "producto": "Panela", "precio": 3500},
    {"id": 10, "producto": "Aceite", "precio": 9500},
    {"id": 11, "producto": "Cafe", "precio": 6000},
    {"id": 12, "producto": "Sal", "precio": 1500},
    {"id": 13, "producto": "Frijol", "precio": 4500},
    {"id": 14, "producto": "Lentejas", "precio": 4000},
    {"id": 15, "producto": "Pasta", "precio": 2500},
    {"id": 16, "producto": "Mantequilla", "precio": 5000},
    {"id": 17, "producto": "Chocolate", "precio": 4500},
    {"id": 18, "producto": "Atun", "precio": 6500},
    {"id": 19, "producto": "Gaseosa", "precio": 3500},
    {"id": 20, "producto": "Jabon", "precio": 3000}
]

while True:
    carro = {}
    print("="*40)
    print("BIENVENIDO A LA TIENDA DE DON JAIRITO")
    print("Escribe listo para finalizar la compra")
    print("="*40)

    print("\n--- DATOS DEL CLIENTE ---")
    nombre_cliente = input("Nombre completo del cliente: ").strip().title()
    cedula_cliente = input("Cédula / Documento: ").strip()
    telefono_cliente = input("Número de teléfono: ").strip()

    carro = {}
    print("\nEscribe 'Listo' cuando termines de agregar productos.")
    while True:
        producto_input = input("Ingrese el nombre del producto o Listo si ya termino: ").strip().title()
        if producto_input == "Listo":
            break

        encontrado = None
        for prod in Inventario:
            if prod["producto"] == producto_input:
                encontrado = prod
                break

        if encontrado:
            try:
                cantidad = int(input(f"Cuantas unidades de {producto_input} desea: "))
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a 0.")
                    continue


                if producto_input in carro:
                    carro[producto_input] += cantidad
                else:
                    carro[producto_input] = cantidad
                print(f"-> {producto_input} anotado. Llevas {carro[producto_input]} en total")
            except ValueError:
                print("Error, Debe ingresar numero entero rey/reina")
        else:
            print(f"Ese producto no esta en el inventario, rey/reina")

    if not carro:
        print("\nNo llevo nada, Vuelve pronto rey/reina")
    else:
        print("\n" + "="*15 + " TIQUETE FINAL " + "="*15)

        print(f"CLIENTE  : {nombre_cliente}")
        print(f"CÉDULA   : {cedula_cliente}")
        print(f"TELÉFONO : {telefono_cliente}")
        print("-" * 45)
        print("DETALLE DEL PEDIDO:")
        print("-" * 45)

        total_compra = 0

        for nombre, cant in carro.items():
            precio_u = 0
            for item in Inventario:
                if item["producto"] == nombre:
                    precio_u = item["precio"]
                    break

            subtotal = precio_u * cant
            total_compra += subtotal
            print(f"{nombre:<14} x{cant:<3}->${subtotal:>9,}")
            
        print("-" * 45)
        print(f"TOTAL A PAGAR:      ${total_compra:>10,}")
        print("-" * 45)
 
        pago = 0
        while pago < total_compra:
            try:
                pago = int(input("\n¿Con cuanto pagas, rey/reina?: "))
                if pago < total_compra:
                   
                    print(f"Faltan $ {total_compra - pago}")
                else:
                    vuelto = pago - total_compra
                    print(f"PAGO RECIBIDO:        ${pago:>10,}")
                    print(f"CAMBIO / DEVOLUCIÓN:  ${vuelto:>10,}")
                    print("\n¡Gracias por su compra!")
            except ValueError:
                print("Ingrese un valor numérico válido para el pago.")

 
    otro = input("\n¿Hay otro cliente? (si/no): ").lower().strip()
    if otro != "si":
        print("Cerrando tienda...")
        break 









