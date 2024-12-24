import tkinter as tk
import sqlite3
import random

# Conectar a la base de datos
conexion = sqlite3.connect("negocios.db")
cursor = conexion.cursor()

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Proveedores (
    codigo_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    producto INTEGER NOT NULL,
    direccion TEXT NOT NULL,
    FOREIGN KEY (producto) REFERENCES Productos(codigo_producto)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Productos (
    codigo_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_producto TEXT NOT NULL,
    descripcion TEXT,
    costo REAL NOT NULL,
    precio REAL NOT NULL,
    caducidad TEXT,
    procedencia TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Clientes (
    codigo_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    cedula TEXT NOT NULL,
    edad INTEGER NOT NULL,
    telefono TEXT NOT NULL,
    direccion TEXT NOT NULL
)
""")

conexion.commit()

# Generar datos para la base de datos
# Insertar 10000 clientes
for i in range(10000):
    nombre = f"Nombre_{i}"
    apellido = f"Apellido_{i}"
    cedula = f"CED{i:05d}"
    edad = random.randint(18, 90)
    telefono = f"555-{random.randint(1000, 9999)}"
    direccion = f"Calle {random.randint(1, 100)}, Ciudad {random.randint(1, 50)}"
    cursor.execute("INSERT INTO Clientes (nombre, apellido, cedula, edad, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?)",
                   (nombre, apellido, cedula, edad, telefono, direccion))

# Insertar 1000 proveedores
for i in range(1000):
    nombre_proveedor = f"Proveedor_{i}"
    direccion_proveedor = f"Avenida {random.randint(1, 50)}, Ciudad {random.randint(1, 20)}"
    cursor.execute("INSERT INTO Proveedores (nombre, producto, direccion) VALUES (?, ?, ?)",
                   (nombre_proveedor, 0, direccion_proveedor))

# Insertar 100 productos por proveedor
for i in range(1000):
    codigo_proveedor = cursor.lastrowid

    # Insertar 100 productos para cada proveedor
    for j in range(100):
        nombre_producto = f"Producto_{i}_{j}"
        descripcion = f"Descripción del producto {j} del proveedor {i}"
        costo = round(random.uniform(10, 100), 2)
        precio = round(costo * random.uniform(1.1, 2.0), 2)
        caducidad = "2025-12-31" if random.choice([True, False]) else None
        procedencia = f"País {random.randint(1, 50)}" if random.choice([True, False]) else None
        cursor.execute("INSERT INTO Productos (nombre_producto, descripcion, costo, precio, caducidad, procedencia) VALUES (?, ?, ?, ?, ?, ?)",
                       (nombre_producto, descripcion, costo, precio, caducidad, procedencia))
        codigo_producto = cursor.lastrowid

        # Asociar el producto al proveedor
        cursor.execute("UPDATE Proveedores SET producto = ? WHERE codigo_proveedor = ?", (codigo_producto, codigo_proveedor))

conexion.commit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aporte Programación")
ventana.geometry("400x400")

# Función para crear una nueva ventana con una barra de búsqueda
def crear_ventana(titulo, tabla):
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("400x300")

    etiqueta = tk.Label(nueva_ventana, text=f"{titulo}", font=("Arial", 14))
    etiqueta.pack(pady=10)

    barra_busqueda = tk.Entry(nueva_ventana, width=30)
    barra_busqueda.pack(pady=10)

    def buscar():
        termino = barra_busqueda.get()
        cursor.execute(f"SELECT * FROM {tabla} WHERE nombre LIKE ?", (f"%{termino}%",))
        resultados = cursor.fetchall()
        for widget in frame_resultados.winfo_children():
            widget.destroy()
        for fila in resultados:
            resultado = tk.Label(frame_resultados, text=fila)
            resultado.pack()

    boton_buscar = tk.Button(nueva_ventana, text="Buscar", command=buscar)
    boton_buscar.pack(pady=10)

    frame_resultados = tk.Frame(nueva_ventana)
    frame_resultados.pack(pady=10)

    boton_regreso = tk.Button(nueva_ventana, text="Regresar", command=nueva_ventana.destroy)
    boton_regreso.pack(pady=10)

# Funciones para manejar los botones
def abrir_proveedores():
    crear_ventana("Proveedores", "Proveedores")

def abrir_productos():
    crear_ventana("Productos", "Productos")

def abrir_clientes():
    crear_ventana("Clientes", "Clientes")

# Crear los botones
btn_proveedores = tk.Button(ventana, text="Proveedores", command=abrir_proveedores, width=20, height=2)
btn_proveedores.pack(pady=10)

btn_productos = tk.Button(ventana, text="Productos", command=abrir_productos, width=20, height=2)
btn_productos.pack(pady=10)

btn_clientes = tk.Button(ventana, text="Clientes", command=abrir_clientes, width=20, height=2)
btn_clientes.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()

# Cerrar la conexión a la base de datos
conexion.close()
