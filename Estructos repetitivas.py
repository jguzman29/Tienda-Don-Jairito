Inventario = [
    {"producto": "Leche", "precio": 4000},
    {"producto": "Huevos", "precio": 1000},
    {"producto": "Arroz", "precio": 2000},
    {"producto": "Pan", "precio": 1000},
    {"producto": "Azucar", "precio": 3500},
    {"producto": "Carne", "precio": 14000},
    {"producto": "Pollo", "precio": 12000},
    {"producto": "Harina", "precio": 3000},
    {"producto": "Panela", "precio": 3500}
]

while True:
    carro = {}
    print("="*40)
    print("BIENVENIDO A LA TIENDA DE DON JAIRITO")
    print("Escribe listo para finalizar la compra")
    print("="*40)

    while True:
        producto = input("Ingrese el nombre del producto o Listo si ya termino: ").strip().title()
        if producto == "Listo":
            break

        encontrado = None
        for prod in Inventario:
            if prod["producto"] == producto:
                encontrado = prod
                break

        if encontrado:
            try:
                cantidad = int(input(f"Cuantas unidades de {producto} desea: "))
                if producto in carro:
                    carro[producto] += cantidad
                else:
                    carro[producto] = cantidad
                print(f"-> {producto} anotado. Llevas {carro[producto]} en total")
            except ValueError:
                print("Error, Debe ingresar numero entero rey/reina")
        else:
            print(f"Ese producto no esta en el inventario, rey/reina")

    if not carro:
        print("\nNo llevo nada, Vuelve pronto rey/reina")
    else:
        print("\n" + "="*12 + " TIQUETE FINAL " + "="*12)
        total_compra = 0

        for nombre, cant in carro.items():
            precio_u = 0
            for item in Inventario:
                if item["producto"] == nombre:
                    precio_u = item["precio"]
                    break

            subtotal = precio_u * cant
            total_compra += subtotal
            print(f"{nombre:<12} x{cant:<3}->${subtotal:>8,}")
            
        print("-" * 39)
        print(f"TOTAL A PAGAR:      ${total_compra:>9,}")
        print("-" * 39)
 
        pago = 0
        while pago < total_compra:
            try:
                pago = int(input("\n¿Con cuanto pagas, rey/reina?: "))
                if pago < total_compra:
                   
                    print(f"Faltan $ {total_compra - pago}")
                else:
                    vuelto = pago - total_compra
                    print(f"\nVuelto: ${vuelto}")
                    print("Gracias por su compra, rey/reina")
            except ValueError:
                print("Ingrese numeros.")

 
    otro = input("\n¿Hay otro cliente? (si/no): ").lower().strip()
    if otro != "si":
        print("Cerrando tienda...")
        break 







