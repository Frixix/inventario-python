import tkinter as tk
from tkinter import ttk, messagebox

# Datos iniciales
productos = {}

def agregar_producto():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    cantidad = entry_cantidad.get()
    precio = entry_precio.get()
    
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

# Ventana principal
root = tk.Tk()
root.title("Inventario Simple")

# Entradas
tk.Label(root, text="Código:").grid(row=0, column=0)
entry_codigo = tk.Entry(root)
entry_codigo.grid(row=0, column=1)

tk.Label(root, text="Nombre:").grid(row=1, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Cantidad:").grid(row=2, column=0)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=2, column=1)

tk.Label(root, text="Precio:").grid(row=3, column=0)
entry_precio = tk.Entry(root)
entry_precio.grid(row=3, column=1)

tk.Button(root, text="Agregar Producto", command=agregar_producto).grid(row=4, column=0, columnspan=2)

# Tabla
tree = ttk.Treeview(root, columns=("Código", "Nombre", "Cantidad", "Precio"), show="headings")
tree.heading("Código", text="Código")
tree.heading("Nombre", text="Nombre")
tree.heading("Cantidad", text="Cantidad")
tree.heading("Precio", text="Precio")
tree.grid(row=5, column=0, columnspan=2)

root.mainloop()
