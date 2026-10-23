import tkinter as tk
from tkinter import ttk, messagebox
from configuracion.base_datos import inicializar_base_datos
from Controladores.mascotas_controlador import MascotaControlador

inicializar_base_datos()

COLOR_BG_MAIN = "#F8FAFC"        
COLOR_SIDEBAR = "#1E293B"        
COLOR_PRIMARY = "#2563EB"        
COLOR_PRIMARY_HOVER = "#1D4ED8"  
COLOR_CARD_BG = "#FFFFFF"        
COLOR_TEXT = "#0F172A"           
COLOR_MUTED = "#64748B"          
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


usuario_actual = {
    "id_usuario": 1,
    "nombre": "Cesar David (Dueño)"
}

def registrar_mascota_interfaz():
    """Toma los datos de la interfaz y se los envía al controlador."""
    nombre = entrada_nombre.get()
    tipo = combo_tipo.get()
    raza = entrada_raza.get()
    edad = entrada_edad.get()
    peso = entrada_peso.get()
    observaciones = entrada_observaciones.get("1.0", tk.END).strip()

    # Llamamos al controlador para validar y guardar en la base de datos
    exito, resultado = MascotaControlador.registrar_mascota(
        usuario_actual["id_usuario"], nombre, tipo, raza, edad, peso, observaciones
    )

    if not exito:
        # Si hay errores de validación, mostramos la alerta
        mensaje = "Por favor revisa los siguientes campos:\n\n" + "\n".join([f"• {e}" for e in resultado])
        messagebox.showerror("Atención", mensaje)
        return

    # Si todo salió bien
    messagebox.showinfo("¡Éxito!", resultado)
    limpiar_formulario()
    mostrar_lista_mascotas()


def limpiar_formulario():
    """Limpia los campos del formulario de registro."""
    entrada_nombre.delete(0, tk.END)
    combo_tipo.set("")
    entrada_raza.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_peso.delete(0, tk.END)
    entrada_observaciones.delete("1.0", tk.END)


def mostrar_formulario():
    """Muestra la vista del formulario para registrar una nueva mascota."""
    limpiar_contenido()

    titulo = tk.Label(
        frame_contenido,
        text="➕ Registrar Nueva Mascota",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    )
    titulo.pack(pady=(30, 20))

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

    lbl_obs = tk.Label(form_frame, text="Observaciones:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_obs.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_observaciones = tk.Text(form_frame, font=FONT_BODY, height=3, bd=1, relief="solid")
    entrada_observaciones.pack(fill="x", padx=25, pady=(0, 20))

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
        command=registrar_mascota_interfaz,
        pady=8
    )
    btn_registrar.pack(fill="x", padx=25, pady=(0, 25))


def mostrar_lista_mascotas():
    """Consulta la base de datos a través del controlador y lista las mascotas del usuario."""
    limpiar_contenido()

    mascotas_usuario = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])

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
            text="Todavía no has registrado ninguna mascota en la base de datos.",
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

    header_frame = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    header_frame.pack(fill="x", padx=40, pady=(30, 10))

    tk.Label(
        header_frame,
        text="🐾 Mis Mascotas (Base de Datos)",
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

        info_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        info_frame.pack(side="left", fill="both")

        tk.Label(
            info_frame,
            text=f"❤️ {m['nombre']}",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"📌 {m['tipo']} ({m['raza']})   •   ⏳ {m['edad']} años   •   ⚖️ {m['peso']} kg",
            font=FONT_BODY,
            bg=COLOR_CARD_BG,
            fg=COLOR_MUTED
        ).pack(anchor="w", pady=(4, 0))

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


def limpiar_contenido():
    """Destruye los widgets anteriores para cambiar de pantalla."""
    for widget in frame_contenido.winfo_children():
        widget.destroy()

ventana = tk.Tk()
ventana.title("Sistema de Gestión de Mascotas - Veterinaria UAN")
ventana.geometry("850x680")
ventana.configure(bg=COLOR_BG_MAIN)


frame_menu = tk.Frame(ventana, width=220, bg=COLOR_SIDEBAR)
frame_menu.pack(side="left", fill="y")
frame_menu.pack_propagate(False)

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

frame_contenido = tk.Frame(ventana, bg=COLOR_BG_MAIN)
frame_contenido.pack(side="right", fill="both", expand=True)

mostrar_lista_mascotas()

ventana.mainloop()
