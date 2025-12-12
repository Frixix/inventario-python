import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# Funciones
# -----------------------
productos = {}

def agregar_producto():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    cantidad = entry_cantidad.get()
    precio = entry_precio.get()
    
    if not codigo or not nombre or not cantidad or not precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    if codigo in productos:
        messagebox.showerror("Error", "El producto ya existe")
        return
    
    productos[codigo] = {
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio
    }
    actualizar_tabla()

    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

def actualizar_tabla():
    for item in tree.get_children():
        tree.delete(item)
    for codigo, info in productos.items():
        tree.insert("", tk.END, values=(codigo, info['nombre'], info['cantidad'], info['precio']))

# -----------------------
# Ventana principal
# -----------------------
root = tk.Tk()
root.title("Inventario Simple")

# Centramos la ventana
ancho, alto = 500, 500
pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()

x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)

root.geometry(f"{ancho}x{alto}+{x}+{y}")
root.configure(bg="#F5F5F5")  # Color suave

# -----------------------
# Estilos
# -----------------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#F5F5F5", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)

# Frame contenedor
frame = ttk.Frame(root, padding=20)
frame.pack(fill="x")

# -----------------------
# Entradas
# -----------------------
ttk.Label(frame, text="Código:").grid(row=0, column=0, sticky="w")
entry_codigo = ttk.Entry(frame)
entry_codigo.grid(row=0, column=1, pady=5, padx=10)

ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="w")
entry_nombre = ttk.Entry(frame)
entry_nombre.grid(row=1, column=1, pady=5, padx=10)

ttk.Label(frame, text="Cantidad:").grid(row=2, column=0, sticky="w")
entry_cantidad = ttk.Entry(frame)
entry_cantidad.grid(row=2, column=1, pady=5, padx=10)

ttk.Label(frame, text="Precio:").grid(row=3, column=0, sticky="w")
entry_precio = ttk.Entry(frame)
entry_precio.grid(row=3, column=1, pady=5, padx=10)

ttk.Button(frame, text="Agregar Producto", command=agregar_producto).grid(row=4, column=0, columnspan=2, pady=15)

# -----------------------
# Tabla
# -----------------------
tree = ttk.Treeview(root, columns=("Código", "Nombre", "Cantidad", "Precio"), show="headings")

for col in ("Código", "Nombre", "Cantidad", "Precio"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True, padx=20, pady=10)

# -----------------------
# Inicia la app
# -----------------------
root.mainloop()
