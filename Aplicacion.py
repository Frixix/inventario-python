import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# Base de datos temporal
# -----------------------
productos = {}

# Lista de códigos de escupideras (NOMBRE + PRECIO placeholder "$%%%")
codigos_escupideras = {
    "ESCL": ("Escupidera Light con tapa", "$%%%"),
    "ESL-B": ("Escupidera Light base", "$%%%"),
    "ESST": ("Escupidera Estándar", "$%%%"),
    "ESST-B": ("Escupidera Estándar base", "$%%%"),
    "ESCB": ("Escupidera Cronos", "$%%%"),
    "ESCB-B": ("Escupidera Cronos base", "$%%%"),
    "ESCHB": ("Escupidera Huevo", "$%%%"),
    "ESCHB-B": ("Escupidera Huevo base", "$%%%"),
    "ESCZ": ("Escupidera Zapato", "$%%%"),
    "ESCZ-B": ("Escupidera Zapato base", "$%%%"),
    "ESCES": ("Escupidera Estándar", "$%%%")
}

# -----------------------
# Funciones
# -----------------------
def agregar_producto():
    codigo = entry_codigo.get().strip().upper()
    nombre = entry_nombre.get().strip()
    cantidad = entry_cantidad.get().strip()
    precio = entry_precio.get().strip()
    categoria = entry_categoria.get().strip()
    
    # Si la categoría es Escupideras, validar que se seleccione al menos la tapa
    if categoria == "Escupideras":
        codigo_tapa = combo_tapa.get().strip().upper()
        if not codigo_tapa:
            messagebox.showerror("Error", "Debes seleccionar una tapa para Escupideras")
            return

    if not codigo or not nombre or not cantidad or not precio or not categoria:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    if codigo in productos:
        messagebox.showerror("Error", "El producto ya existe")
        return
    
    productos[codigo] = {
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'categoria': categoria
    }

    actualizar_tabla()

    # limpiar campos
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)

    # limpiar y ocultar combobox
    combo_codigos.set("")
    combo_codigos.grid_remove()
    
    # Limpiar tapa y base
    combo_tapa.set("")
    combo_base.set("")
    label_base_info.config(text="")


def actualizar_tabla():
    for item in tree.get_children():
        tree.delete(item)
    for codigo, info in productos.items():
        tree.insert("", tk.END, values=(
            codigo, 
            info['nombre'], 
            info['cantidad'], 
            info['precio'], 
            info['categoria']
        ))


def set_categoria(cat):
    entry_categoria.delete(0, tk.END)
    entry_categoria.insert(0, cat)

    # Si selecciona Escupideras → mostrar combo en la misma fila del código
    if cat == "Escupideras":
        combo_codigos['values'] = list(codigos_escupideras.keys())
        combo_codigos.grid(row=0, column=2, padx=(10,0), pady=5, sticky="w")
        
        # Separar tapas y bases
        tapas = [cod for cod in codigos_escupideras.keys() if not cod.endswith("-B")]
        bases = [cod for cod in codigos_escupideras.keys() if cod.endswith("-B")]
        
        # Mostrar secciones de tapa y base
        combo_tapa['values'] = tapas
        combo_base['values'] = bases
        
        label_tapa.grid()
        combo_tapa.grid()
        label_base.grid()
        combo_base.grid()
    else:
        combo_codigos.grid_remove()
        combo_codigos.set("")
        # Ocultar secciones de tapa y base
        label_tapa.grid_remove()
        combo_tapa.grid_remove()
        label_base.grid_remove()
        combo_base.grid_remove()
        combo_tapa.set("")
        combo_base.set("")
        label_base_info.config(text="")


def obtener_codigo_base(codigo_tapa):
    """Obtiene el código de la base correspondiente a una tapa"""
    # Si el código no termina en -B, agregamos -B
    if not codigo_tapa.endswith("-B"):
        codigo_base = codigo_tapa + "-B"
        # Verificar si existe en la lista de escupideras
        if codigo_base in codigos_escupideras:
            return codigo_base
    return None


def obtener_codigo_tapa(codigo_base):
    """Obtiene el código de la tapa correspondiente a una base"""
    # Si el código termina en -B, lo removemos
    if codigo_base.endswith("-B"):
        codigo_tapa = codigo_base[:-2]
        # Verificar si existe en la lista de escupideras
        if codigo_tapa in codigos_escupideras:
            return codigo_tapa
    return None


def seleccionar_codigo_tapa(event):
    """Cuando el usuario selecciona una tapa"""
    codigo_tapa = combo_tapa.get().strip().upper()
    
    if codigo_tapa in codigos_escupideras:
        nombre_tapa, precio_tapa = codigos_escupideras[codigo_tapa]
        
        # Autocompletar el código principal con la tapa
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo_tapa)
        
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, nombre_tapa)
        
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, precio_tapa)
        
        # Sugerir la base correspondiente
        codigo_base = obtener_codigo_base(codigo_tapa)
        if codigo_base:
            # Mostrar automáticamente la base en el combo_base
            combo_base.set(codigo_base)
            # Mostrar también el nombre y precio de la base
            nombre_base, precio_base = codigos_escupideras[codigo_base]
            label_base_info.config(text=f"{nombre_base} - {precio_base}")


def seleccionar_codigo_base(event):
    """Cuando el usuario selecciona una base"""
    codigo_base = combo_base.get().strip().upper()
    
    if codigo_base in codigos_escupideras:
        nombre_base, precio_base = codigos_escupideras[codigo_base]
        label_base_info.config(text=f"{nombre_base} - {precio_base}")


def seleccionar_codigo(event):
    codigo = combo_codigos.get().strip().upper()

    # autocompletar campos si el código está en la lista de escupideras
    if codigo in codigos_escupideras:
        nombre, precio = codigos_escupideras[codigo]

        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, nombre)

        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, precio)


# -----------------------
# Ventana principal
# -----------------------
root = tk.Tk()
root.title("Inventario Mejorado")

root.geometry("700x620")
root.configure(bg="#F5F5F5")

# -----------------------
# Estilos
# -----------------------
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#F5F5F5", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10), padding=4)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)

# -----------------------
# Frame Entradas
# -----------------------
frame = ttk.Frame(root, padding=12)
frame.pack(fill="x")

# Código (col 0,1) - el combobox aparecerá en col 2 de este mismo frame
ttk.Label(frame, text="Código:").grid(row=0, column=0, sticky="w")
entry_codigo = ttk.Entry(frame)
entry_codigo.grid(row=0, column=1, pady=5, padx=10, sticky="w")

# Combobox (oculto al inicio). Está en el mismo 'frame' para usar grid coherentemente.
combo_codigos = ttk.Combobox(frame, state="readonly", width=20)
combo_codigos.bind("<<ComboboxSelected>>", seleccionar_codigo)
combo_codigos.grid(row=0, column=2, padx=(10,0), pady=5, sticky="w")
combo_codigos.grid_remove()  # ocultarlo inicialmente

# Nombre
ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="w")
entry_nombre = ttk.Entry(frame, width=40)
entry_nombre.grid(row=1, column=1, columnspan=2, pady=5, padx=10, sticky="w")

# Cantidad
ttk.Label(frame, text="Cantidad:").grid(row=2, column=0, sticky="w")
entry_cantidad = ttk.Entry(frame)
entry_cantidad.grid(row=2, column=1, pady=5, padx=10, sticky="w")

# Precio
ttk.Label(frame, text="Precio:").grid(row=3, column=0, sticky="w")
entry_precio = ttk.Entry(frame)
entry_precio.grid(row=3, column=1, pady=5, padx=10, sticky="w")

# Categoría (se llenará al presionar botón)
ttk.Label(frame, text="Categoría:").grid(row=4, column=0, sticky="w")
entry_categoria = ttk.Entry(frame)
entry_categoria.grid(row=4, column=1, pady=5, padx=10, sticky="w")

# -----------------------
# Sección de Tapa y Base (inicialmente oculta)
# -----------------------
frame_tapa_base = ttk.LabelFrame(root, text="Selecciona Tapa y Base", padding=12)
frame_tapa_base.pack(fill="x", padx=20, pady=(10,0))

# Tapa
label_tapa = ttk.Label(frame_tapa_base, text="Tapa:")
label_tapa.grid(row=0, column=0, sticky="w", pady=5)

combo_tapa = ttk.Combobox(frame_tapa_base, state="readonly", width=30)
combo_tapa.bind("<<ComboboxSelected>>", seleccionar_codigo_tapa)
combo_tapa.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_tapa.grid_remove()
combo_tapa.grid_remove()

# Base
label_base = ttk.Label(frame_tapa_base, text="Base:")
label_base.grid(row=1, column=0, sticky="w", pady=5)

combo_base = ttk.Combobox(frame_tapa_base, state="readonly", width=30)
combo_base.bind("<<ComboboxSelected>>", seleccionar_codigo_base)
combo_base.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_base_info = ttk.Label(frame_tapa_base, text="", foreground="green")
label_base_info.grid(row=1, column=2, padx=10, pady=5, sticky="w")

label_base.grid_remove()
combo_base.grid_remove()

# -----------------------
# Botones de Categoría (mejorados y más pequeños)
# -----------------------
frame_categorias = ttk.Frame(root, padding=(10,0,10,10))
frame_categorias.pack(fill="x")

botones = [
    ("Escupideras", "#7EBCF1"),
    ("Módulos", "#FFA54D"),
    ("Guardas", "#CFCFCF"),
    ("Otros", "#FFE26F"),
    ("Plataformas", "#8EF28C")
]

for texto, color in botones:
    b = tk.Button(
        frame_categorias,
        text=texto,
        bg=color,
        fg="black",
        width=11,
        height=1,
        font=("Segoe UI", 9),
        relief="raised",
        bd=1,
        command=lambda c=texto: set_categoria(c)
    )
    b.pack(side="left", padx=6, pady=6)

# -----------------------
# Botón Agregar
# -----------------------
ttk.Button(frame, text="Agregar Producto", command=agregar_producto).grid(row=5, column=0, columnspan=3, pady=14)

# -----------------------
# Tabla
# -----------------------
tree = ttk.Treeview(
    root, 
    columns=("Código", "Nombre", "Cantidad", "Precio", "Categoría"), 
    show="headings",
    height=12
)

for col in ("Código", "Nombre", "Cantidad", "Precio", "Categoría"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True, padx=20, pady=(0,20))

root.mainloop()
