from estructuras import inicializar_bd, SessionLocal, Cliente, Producto, Venta, DetalleVenta

def ejecutar_tienda():
    if not inicializar_bd():
        print("No se pudo conectar a la BD. Revisa las credenciales.")
        return

    while True:
        session = SessionLocal()
        print("="*40)
        print("      BIENVENIDO A LA TIENDA DE DON JAIRITO")
        print("="*40)


        print("\n--- DATOS DEL CLIENTE ---")
        cedula_in = input("Cédula / Documento: ").strip()
        cliente = session.query(Cliente).filter_by(cedula=cedula_in).first()

        if not cliente:
            nombre_in = input("Nombre completo del cliente: ").strip().title()
            telefono_in = input("Número de teléfono: ").strip()
            cliente = Cliente(cedula=cedula_in, nombre=nombre_in, telefono=telefono_in)
            session.add(cliente)
            session.commit()
            print("-> Cliente registrado exitosamente en la BD.")
        else:
            print(f"-> Cliente encontrado: {cliente.nombre}")

        carro = {}

        while True:
            prod_input = input("\nIngrese producto (o 'Listo' para finalizar): ").strip().title()
            if prod_input == "Listo":
                break

            producto_obj = session.query(Producto).filter_by(nombre=prod_input).first()

            if producto_obj:
                try:
                    cant = int(input(f"¿Cuántas unidades de {prod_input} desea?: "))
                    if cant <= 0:
                        print("La cantidad debe ser mayor a 0.")
                        continue
                    
                    if producto_obj.id in carro:
                        carro[producto_obj.id]["cantidad"] += cant
                    else:
                        carro[producto_obj.id] = {"obj": producto_obj, "cantidad": cant}
                    print(f"-> {prod_input} anotado. Llevas {carro[producto_obj.id]['cantidad']} en total.")
                except ValueError:
                    print("Error: Ingrese un entero válido.")
            else:
                print("Ese producto no está en el inventario.")

       
        if carro:
            print("\n" + "="*15 + " TIQUETE FINAL " + "="*15)
            print(f"CLIENTE  : {cliente.nombre}")
            print(f"CÉDULA   : {cliente.cedula}")
            print(f"TELÉFONO : {cliente.telefono}")
            print("-" * 45)
            print("DETALLE DEL PEDIDO:")
            print("-" * 45)

            total_compra = 0
            nueva_venta = Venta(cedula_cliente=cliente.cedula, total=0)
            session.add(nueva_venta)
            session.flush()

            for item in carro.values():
                prod = item["obj"]
                cant = item["cantidad"]
                subtotal = prod.precio * cant
                total_compra += subtotal

                detalle = DetalleVenta(
                    id_venta=nueva_venta.id,
                    id_producto=prod.id,
                    cantidad=cant,
                    subtotal=subtotal
                )
                session.add(detalle)
                print(f"{prod.nombre:<14} x{cant:<3} -> ${subtotal:>9,}")

            nueva_venta.total = total_compra
            session.commit()

            print("-" * 45)
            print(f"TOTAL A PAGAR:        ${total_compra:>10,}")
            print("-" * 45)

            pago = 0
            while pago < total_compra:
                try:
                    pago = int(input("\n¿Con cuánto paga el cliente?: $"))
                    if pago < total_compra:
                        print(f"Faltan ${total_compra - pago:,}")
                    else:
                        vuelto = pago - total_compra
                        print(f"PAGO RECIBIDO:        ${pago:>10,}")
                        print(f"CAMBIO / DEVOLUCIÓN:  ${vuelto:>10,}")
                        print("\n¡Gracias por su compra! Venta guardada en BD.")
                except ValueError:
                    print("Ingrese un número válido.")

        session.close()
        otro = input("\n¿Hay otro cliente? (si/no): ").lower().strip()
        if otro != "si":
            print("\nCerrando tienda...")
            break

if __name__ == "__main__":
    ejecutar_tienda()