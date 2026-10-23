import tkinter as tk
from tkinter import ttk, messagebox

# ESTILOS Y PALETA PROVISIONAL
COLOR_BG_MAIN = "#F8FAFC"        # Fondo general gris muy claro
COLOR_SIDEBAR = "#1E293B"        # Azul oscuro elegante para el menú
COLOR_PRIMARY = "#2563EB"        # Azul principal para botones
COLOR_PRIMARY_HOVER = "#1D4ED8"  # Azul oscuro al pasar el mouse
COLOR_CARD_BG = "#FFFFFF"        # Blanco para tarjetas
COLOR_TEXT = "#0F172A"           # Texto oscuro principal
COLOR_MUTED = "#64748B"          # Texto secundario/gris
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

# REGISTRO DE PRUEBA

mascotas = [
    {
        "id_mascota": 1,
        "id_usuario": 1,
        "nombre": "Mascota de prueba",
        "tipo": "Perro",
        "raza": "Labrador",
        "edad": 3,
        "peso": 12.5,
        "foto": None,
        "observaciones": "Padece asma"
    }
]

usuario_actual = {
    "id_usuario": 1,
    "nombre": "Usuario x (temporal)"
}


# FUNCIONES DE DATOS
def obtener_mascotas_usuario(id_usuario):
    return [m for m in mascotas if m["id_usuario"] == id_usuario]

def obtener_mascota_por_id(id_mascota):
    for m in mascotas:
        if m["id_mascota"] == id_mascota:
            return m
    return None



# Exepciones

def validar_datos(nombre, tipo, raza, edad, peso):
    errores = []
    if not nombre.strip():
        errores.append("El nombre es obligatorio.")
    if not tipo.strip():
        errores.append("El tipo de mascota es obligatorio.")
    if not raza.strip():
        errores.append("La raza es obligatoria.")

    try:
        edad_num = int(edad)
        if edad_num < 0:
            errores.append("La edad no puede ser negativa.")
    except ValueError:
        errores.append("La edad debe ser un número entero.")

    try:
        peso_num = float(peso)
        if peso_num <= 0:
            errores.append("El peso debe ser mayor que 0.")
    except ValueError:
        errores.append("El peso debe ser un número.")

    return errores


# REGISTRAR MASCOTA

def registrar_mascota():
    nombre = entrada_nombre.get()
    tipo = combo_tipo.get()
    raza = entrada_raza.get()
    edad = entrada_edad.get()
    peso = entrada_peso.get()
    observaciones = entrada_observaciones.get("1.0", tk.END).strip()

    errores = validar_datos(nombre, tipo, raza, edad, peso)

    if errores:
        mensaje = "Por favor revisa los siguientes campos:\n\n" + "\n".join([f"• {e}" for e in errores])
        messagebox.showerror("Atención", mensaje)
        return

    nuevo_id = len(mascotas) + 1
    nueva_mascota = {
        "id_mascota": nuevo_id,
        "id_usuario": usuario_actual["id_usuario"],
        "nombre": nombre,
        "tipo": tipo,
        "raza": raza,
        "edad": int(edad),
        "peso": float(peso),
        "foto": None,
        "observaciones": observaciones
    }

    mascotas.append(nueva_mascota)
    messagebox.showinfo("¡Éxito!", f"¡{nombre}  Mascota registrada correctamente!")
    limpiar_formulario()
    mostrar_lista_mascotas()


# ============================================================
# LIMPIAR FORMULARIO
# ============================================================
def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    combo_tipo.set("")
    entrada_raza.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_peso.delete(0, tk.END)
    entrada_observaciones.delete("1.0", tk.END)


# FUNCION MOSTRAR FORMULARIO

def mostrar_formulario():
    limpiar_contenido()

    titulo = tk.Label(
        frame_contenido,
        text="➕ Registrar Nueva Mascota",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    )
    titulo.pack(pady=(30, 20))

    # Formulario contenedor
    form_frame = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", highlightthickness=0)
    form_frame.pack(padx=60, pady=10, fill="x")

    def crear_campo(parent, texto):
        label = tk.Label(parent, text=texto, font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
        label.pack(anchor="w", padx=25, pady=(12, 2))
        entry = tk.Entry(parent, font=FONT_BODY, bd=1, relief="solid")
        entry.pack(fill="x", padx=25, pady=(0, 5), ipady=4)
        return entry

    global entrada_nombre, combo_tipo, entrada_raza, entrada_edad, entrada_peso, entrada_observaciones

    entrada_nombre = crear_campo(form_frame, "Nombre de la mascota:")

    # Combo Tipo
    lbl_tipo = tk.Label(form_frame, text="Tipo de mascota:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_tipo.pack(anchor="w", padx=25, pady=(12, 2))
    combo_tipo = ttk.Combobox(
        form_frame,
        values=["Perro 🐶", "Gato 🐱", "Ave 🦜", "Conejo 🐰", "Otro 🐾"],
        state="readonly",
        font=FONT_BODY
    )
    combo_tipo.pack(fill="x", padx=25, pady=(0, 5), ipady=2)

    entrada_raza = crear_campo(form_frame, "Raza:")
    entrada_edad = crear_campo(form_frame, "Edad (años):")
    entrada_peso = crear_campo(form_frame, "Peso (kg):")

    # Observaciones
    lbl_obs = tk.Label(form_frame, text="Observaciones:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_obs.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_observaciones = tk.Text(form_frame, font=FONT_BODY, height=3, bd=1, relief="solid")
    entrada_observaciones.pack(fill="x", padx=25, pady=(0, 20))

    # Botón de Guardado
    btn_registrar = tk.Button(
        form_frame,
        text="💾 Guardar Mascota",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=registrar_mascota,
        pady=8
    )
    btn_registrar.pack(fill="x", padx=25, pady=(0, 25))



# MOSTRAR LISTA DE MASCOTAS
def mostrar_lista_mascotas():
    limpiar_contenido()

    mascotas_usuario = obtener_mascotas_usuario(usuario_actual["id_usuario"])

    # CONDICION DE SI NO HAY MASCOTAS

    if not mascotas_usuario:
        tk.Label(
            frame_contenido,
            text="🐶 ¡Bienvenido!",
            font=FONT_TITLE,
            bg=COLOR_BG_MAIN,
            fg=COLOR_TEXT
        ).pack(pady=(100, 10))

        tk.Label(
            frame_contenido,
            text="Todavía no has registrado ninguna mascota.",
            font=FONT_BODY,
            bg=COLOR_BG_MAIN,
            fg=COLOR_MUTED
        ).pack(pady=5)

        tk.Button(
            frame_contenido,
            text="➕ Registrar Mascota",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=mostrar_formulario
        ).pack(pady=25)
        return

    # INFO MASCOTAS
    header_frame = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    header_frame.pack(fill="x", padx=40, pady=(30, 10))

    tk.Label(
        header_frame,
        text="🐾 Mis Mascotas",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    ).pack(side="left")

    tk.Label(
        header_frame,
        text=f"Total: {len(mascotas_usuario)}",
        font=FONT_SUBTITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_MUTED
    ).pack(side="right")

    frame_lista = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    frame_lista.pack(fill="both", expand=True, padx=40, pady=10)

    for m in mascotas_usuario:
        card = tk.Frame(
            frame_lista,
            bg=COLOR_CARD_BG,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        card.pack(fill="x", pady=8)

        # Información izquierda
        info_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        info_frame.pack(side="left", fill="both")

        lbl_nombre = tk.Label(
            info_frame,
            text=f"❤️ {m['nombre']}",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT
        )
        lbl_nombre.pack(anchor="w")

        lbl_detalles = tk.Label(
            info_frame,
            text=f"📌 {m['tipo']} ({m['raza']})   •   ⏳ {m['edad']} años   •   ⚖️ {m['peso']} kg",
            font=FONT_BODY,
            bg=COLOR_CARD_BG,
            fg=COLOR_MUTED
        )
        lbl_detalles.pack(anchor="w", pady=(4, 0))

        # Botón Perfil
        tk.Button(
            card,
            text="Ver Perfil ➔",
            font=FONT_BOLD,
            bg="#EFF6FF",
            fg=COLOR_PRIMARY,
            activebackground="#DBEAFE",
            activeforeground=COLOR_PRIMARY,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda id_mascota=m["id_mascota"]: mostrar_perfil(id_mascota)
        ).pack(side="right")

    # Botón de agregado
    tk.Button(
        frame_contenido,
        text="➕ Registrar Nueva Mascota",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=10,
        command=mostrar_formulario
    ).pack(pady=20)



# PERFIL DE MASCOTA
def mostrar_perfil(id_mascota):
    mascota = obtener_mascota_por_id(id_mascota)

    if mascota is None:
        messagebox.showerror("Error", "No se encontró la mascota.")
        return

    limpiar_contenido()

    tk.Label(
        frame_contenido,
        text=f"📋 Perfil de {mascota['nombre']}",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    ).pack(pady=(40, 20))

    card = tk.Frame(
        frame_contenido,
        bg=COLOR_CARD_BG,
        bd=1,
        relief="solid",
        padx=30,
        pady=25
    )
    card.pack(padx=80, fill="x")

    def fila_info(parent, etiqueta, valor):
        f = tk.Frame(parent, bg=COLOR_CARD_BG)
        f.pack(fill="x", pady=6)
        tk.Label(f, text=etiqueta, font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_MUTED, width=15, anchor="w").pack(side="left")
        tk.Label(f, text=valor, font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT).pack(side="left")

    fila_info(card, "Nombre:", mascota['nombre'])
    fila_info(card, "Tipo:", mascota['tipo'])
    fila_info(card, "Raza:", mascota['raza'])
    fila_info(card, "Edad:", f"{mascota['edad']} años")
    fila_info(card, "Peso:", f"{mascota['peso']} kg")

    tk.Frame(card, bg="#E2E8F0", height=1).pack(fill="x", pady=15)

    tk.Label(card, text="Observaciones:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_MUTED).pack(anchor="w")
    tk.Label(
        card,
        text=mascota['observaciones'] or "Sin observaciones registradas.",
        font=FONT_BODY,
        bg=COLOR_CARD_BG,
        fg=COLOR_TEXT,
        wraplength=450,
        justify="left"
    ).pack(anchor="w", pady=(5, 0))

    tk.Button(
        frame_contenido,
        text="⬅️ Volver a mis mascotas",
        font=FONT_BOLD,
        bg="#E2E8F0",
        fg=COLOR_TEXT,
        activebackground="#CBD5E1",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=8,
        command=mostrar_lista_mascotas
    ).pack(pady=25)



# Para limpiar contenido
def limpiar_contenido():
    for widget in frame_contenido.winfo_children():
        widget.destroy()


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Mascotas")
ventana.geometry("850x680")
ventana.configure(bg=COLOR_BG_MAIN)

# MENÚ LATERAL (SIDEBAR)
frame_menu = tk.Frame(ventana, width=220, bg=COLOR_SIDEBAR)
frame_menu.pack(side="left", fill="y")
frame_menu.pack_propagate(False)

# Título Sidebar
tk.Label(
    frame_menu,
    text="VETERINARIA",
    font=("Segoe UI", 18, "bold"),
    bg=COLOR_SIDEBAR,
    fg="white"
).pack(pady=(40, 5))

tk.Label(
    frame_menu,
    text=f"Hola, {usuario_actual['nombre']} 👋",
    font=FONT_BODY,
    bg=COLOR_SIDEBAR,
    fg="#94A3B8"
).pack(pady=(0, 30))

# Botones de navegación
btn_mis_mascotas = tk.Button(
    frame_menu,
    text="🐾  Mis Mascotas",
    font=FONT_BOLD,
    bg=COLOR_SIDEBAR,
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    bd=0,
    anchor="w",
    padx=25,
    cursor="hand2",
    command=mostrar_lista_mascotas
)
btn_mis_mascotas.pack(fill="x", pady=5, ipady=8)

btn_agregar = tk.Button(
    frame_menu,
    text="➕  Agregar Mascota",
    font=FONT_BOLD,
    bg=COLOR_SIDEBAR,
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    bd=0,
    anchor="w",
    padx=25,
    cursor="hand2",
    command=mostrar_formulario
)
btn_agregar.pack(fill="x", pady=5, ipady=8)



# CONTENIDO PRINCIPAL

frame_contenido = tk.Frame(ventana, bg=COLOR_BG_MAIN)
frame_contenido.pack(side="right", fill="both", expand=True)


# ACTIVAR INICIO

mostrar_lista_mascotas()

ventana.mainloop()


