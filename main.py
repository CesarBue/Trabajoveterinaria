import tkinter as tk
from tkinter import ttk, messagebox
from configuracion.base_datos import inicializar_base_datos
from controladores.mascotas_controlador import MascotaControlador
from controladores.reserva_controlador import ReservaControlador
from controladores.historial_controlador import HistorialControlador

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

# USUARIO ACTUAL (Temporal para demostración)
usuario_actual = {
    "id_usuario": 1,
    "nombre": "Cesar David (Dueño)"
}


def registrar_mascota_interfaz():
    nombre = entrada_nombre.get()
    tipo = combo_tipo.get()
    raza = entrada_raza.get()
    edad = entrada_edad.get()
    peso = entrada_peso.get()
    observaciones = entrada_observaciones.get("1.0", tk.END).strip()

    exito, resultado = MascotaControlador.registrar_mascota(
        usuario_actual["id_usuario"], nombre, tipo, raza, edad, peso, observaciones
    )

    if not exito:
        mensaje = "Por favor revisa los siguientes campos:\n\n" + "\n".join([f"• {e}" for e in resultado])
        messagebox.showerror("Atención", mensaje)
        return

    messagebox.showinfo("¡Éxito!", resultado)
    limpiar_formulario()
    mostrar_lista_mascotas()


def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    combo_tipo.set("")
    entrada_raza.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_peso.delete(0, tk.END)
    entrada_observaciones.delete("1.0", tk.END)


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

    form_frame = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid")
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



def registrar_reserva_interfaz():
    seleccion_mascota = combo_mascotas_reserva.get()
    if not seleccion_mascota:
        messagebox.showerror("Atención", "Debes seleccionar una mascota.")
        return
    
    id_mascota = seleccion_mascota.split(" - ")[0]
    servicio = combo_servicio_reserva.get()
    fecha = entrada_fecha.get()
    costo = entrada_costo.get()

    exito, mensaje = ReservaControlador.registrar_reserva(
        id_mascota, servicio, fecha, costo
    )

    if not exito:
        messagebox.showerror("Atención", mensaje)
        return

    messagebox.showinfo("¡Éxito!", mensaje)
    mostrar_lista_reservas()


def mostrar_formulario_reserva():
    limpiar_contenido()

    titulo = tk.Label(
        frame_contenido,
        text="📅 Agendar Cita o Guardería",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    )
    titulo.pack(pady=(30, 20))

    form_frame = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid")
    form_frame.pack(padx=60, pady=10, fill="x")

    mascotas_usuario = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])
    nombres_mascotas = [f"{m['id_mascota']} - {m['nombre']} ({m['tipo']})" for m in mascotas_usuario]

    if not nombres_mascotas:
        messagebox.showwarning("Aviso", "Primero debes registrar al menos una mascota.")
        mostrar_formulario()
        return

    lbl_mascota = tk.Label(form_frame, text="Seleccionar Mascota:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_mascota.pack(anchor="w", padx=25, pady=(12, 2))
    global combo_mascotas_reserva
    combo_mascotas_reserva = ttk.Combobox(form_frame, values=nombres_mascotas, state="readonly", font=FONT_BODY)
    combo_mascotas_reserva.pack(fill="x", padx=25, pady=(0, 5), ipady=2)

    lbl_servicio = tk.Label(form_frame, text="Servicio requerido:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_servicio.pack(anchor="w", padx=25, pady=(12, 2))
    global combo_servicio_reserva
    combo_servicio_reserva = ttk.Combobox(
        form_frame,
        values=["Consulta Médica 🩺", "Guardería 🏡", "Peluquería / Baño ✂️", "Vacunación 💉"],
        state="readonly",
        font=FONT_BODY
    )
    combo_servicio_reserva.pack(fill="x", padx=25, pady=(0, 5), ipady=2)

    global entrada_fecha, entrada_costo
    lbl_fecha = tk.Label(form_frame, text="Fecha y hora (YYYY-MM-DD HH:MM):", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_fecha.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_fecha = tk.Entry(form_frame, font=FONT_BODY, bd=1, relief="solid")
    entrada_fecha.pack(fill="x", padx=25, pady=(0, 5), ipady=4)

    lbl_costo = tk.Label(form_frame, text="Costo estimado ($):", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_costo.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_costo = tk.Entry(form_frame, font=FONT_BODY, bd=1, relief="solid")
    entrada_costo.pack(fill="x", padx=25, pady=(0, 20), ipady=4)

    btn_guardar_reserva = tk.Button(
        form_frame,
        text="📅 Confirmar Reserva",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=registrar_reserva_interfaz,
        pady=8
    )
    btn_guardar_reserva.pack(fill="x", padx=25, pady=(0, 25))


def mostrar_lista_reservas():
    limpiar_contenido()

    reservas = ReservaControlador.obtener_reservas_por_usuario(usuario_actual["id_usuario"])

    header_frame = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    header_frame.pack(fill="x", padx=40, pady=(30, 10))

    tk.Label(
        header_frame,
        text="📅 Mis Reservas y Citas",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    ).pack(side="left")

    tk.Button(
        header_frame,
        text="➕ Nueva Reserva",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=5,
        command=mostrar_formulario_reserva
    ).pack(side="right")

    if not reservas:
        tk.Label(
            frame_contenido,
            text="No tienes ninguna cita o reserva registrada.",
            font=FONT_BODY,
            bg=COLOR_BG_MAIN,
            fg=COLOR_MUTED
        ).pack(pady=40)
        return

    frame_lista = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    frame_lista.pack(fill="both", expand=True, padx=40, pady=10)

    for r in reservas:
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
            text=f"🐾 Mascota: {r['nombre_mascota']} — Servicio: {r['servicio']}",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"📌 Fecha: {r['fecha_reserva']}   •   💰 Costo: ${r['costo_estimado']}   •   🔹 Estado: {r['estado']}",
            font=FONT_BODY,
            bg=COLOR_CARD_BG,
            fg=COLOR_MUTED
        ).pack(anchor="w", pady=(4, 0))



def registrar_historial_interfaz():
    seleccion_mascota = combo_mascotas_historial.get()
    if not seleccion_mascota:
        messagebox.showerror("Atención", "Debes seleccionar una mascota.")
        return
    
    id_mascota = seleccion_mascota.split(" - ")[0]
    tipo_registro = combo_tipo_historial.get()
    descripcion = entrada_desc_historial.get("1.0", tk.END).strip()
    fecha = entrada_fecha_historial.get()

    exito, resultado = HistorialControlador.registrar_historial(
        id_mascota, tipo_registro, descripcion, fecha
    )

    if not exito:
        mensaje = "Por favor revisa los siguientes campos:\n\n" + "\n".join([f"• {e}" for e in resultado])
        messagebox.showerror("Atención", mensaje)
        return

    messagebox.showinfo("¡Éxito!", resultado)
    mostrar_lista_historial()


def mostrar_formulario_historial():
    limpiar_contenido()

    titulo = tk.Label(
        frame_contenido,
        text="💉 Registrar Vacuna o Historial Médico",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    )
    titulo.pack(pady=(30, 20))

    form_frame = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid")
    form_frame.pack(padx=60, pady=10, fill="x")

    mascotas_usuario = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])
    nombres_mascotas = [f"{m['id_mascota']} - {m['nombre']} ({m['tipo']})" for m in mascotas_usuario]

    if not nombres_mascotas:
        messagebox.showwarning("Aviso", "Primero debes registrar al menos una mascota.")
        mostrar_formulario()
        return

    lbl_mascota = tk.Label(form_frame, text="Seleccionar Mascota:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_mascota.pack(anchor="w", padx=25, pady=(12, 2))
    global combo_mascotas_historial
    combo_mascotas_historial = ttk.Combobox(form_frame, values=nombres_mascotas, state="readonly", font=FONT_BODY)
    combo_mascotas_historial.pack(fill="x", padx=25, pady=(0, 5), ipady=2)

    lbl_tipo = tk.Label(form_frame, text="Tipo de Registro:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_tipo.pack(anchor="w", padx=25, pady=(12, 2))
    global combo_tipo_historial
    combo_tipo_historial = ttk.Combobox(
        form_frame,
        values=["Vacuna 💉", "Desparasitación 💊", "Consulta Médica 🩺", "Examen 🔬"],
        state="readonly",
        font=FONT_BODY
    )
    combo_tipo_historial.pack(fill="x", padx=25, pady=(0, 5), ipady=2)

    global entrada_desc_historial, entrada_fecha_historial
    lbl_desc = tk.Label(form_frame, text="Descripción / Observación:", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_desc.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_desc_historial = tk.Text(form_frame, font=FONT_BODY, height=3, bd=1, relief="solid")
    entrada_desc_historial.pack(fill="x", padx=25, pady=(0, 5))

    lbl_fecha = tk.Label(form_frame, text="Fecha (YYYY-MM-DD):", font=FONT_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT)
    lbl_fecha.pack(anchor="w", padx=25, pady=(12, 2))
    entrada_fecha_historial = tk.Entry(form_frame, font=FONT_BODY, bd=1, relief="solid")
    entrada_fecha_historial.pack(fill="x", padx=25, pady=(0, 20), ipady=4)

    btn_guardar = tk.Button(
        form_frame,
        text="💾 Guardar en Historial",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=registrar_historial_interfaz,
        pady=8
    )
    btn_guardar.pack(fill="x", padx=25, pady=(0, 25))


def mostrar_lista_historial():
    limpiar_contenido()

    header_frame = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    header_frame.pack(fill="x", padx=40, pady=(30, 10))

    tk.Label(
        header_frame,
        text="📋 Historial Médico y Vacunas",
        font=FONT_TITLE,
        bg=COLOR_BG_MAIN,
        fg=COLOR_TEXT
    ).pack(side="left")

    tk.Button(
        header_frame,
        text="➕ Nuevo Registro",
        font=FONT_BOLD,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_PRIMARY_HOVER,
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=5,
        command=mostrar_formulario_historial
    ).pack(side="right")

    mascotas_usuario = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])
    if not mascotas_usuario:
        tk.Label(
            frame_contenido,
            text="No hay mascotas registradas para ver historiales.",
            font=FONT_BODY,
            bg=COLOR_BG_MAIN,
            fg=COLOR_MUTED
        ).pack(pady=40)
        return

    frame_lista = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    frame_lista.pack(fill="both", expand=True, padx=40, pady=10)

    for m in mascotas_usuario:
        historiales = HistorialControlador.obtener_historial_por_mascota(m["id_mascota"])
        
        card_mascota = tk.Frame(frame_lista, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=10)
        card_mascota.pack(fill="x", pady=6)

        tk.Label(
            card_mascota,
            text=f"🐾 Mascota: {m['nombre']} ({m['tipo']})",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_PRIMARY
        ).pack(anchor="w", pady=(0, 5))

        if not historiales:
            tk.Label(
                card_mascota,
                text="Sin registros médicos o vacunas aún.",
                font=FONT_BODY,
                bg=COLOR_CARD_BG,
                fg=COLOR_MUTED
            ).pack(anchor="w", padx=10)
        else:
            for h in historiales:
                tk.Label(
                    card_mascota,
                    text=f"• [{h['fecha']}] {h['tipo_registro']}: {h['descripcion']}",
                    font=FONT_BODY,
                    bg=COLOR_CARD_BG,
                    fg=COLOR_TEXT
                ).pack(anchor="w", padx=10, pady=2)


def limpiar_contenido():
    for widget in frame_contenido.winfo_children():
        widget.destroy()


ventana = tk.Tk()
ventana.title("Sistema de Gestión de Mascotas - Veterinaria UAN")
ventana.geometry("900x700")
ventana.configure(bg=COLOR_BG_MAIN)

frame_menu = tk.Frame(ventana, width=230, bg=COLOR_SIDEBAR)
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

tk.Button(
    frame_menu, text="🐾  Mis Mascotas", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white",
    activebackground="#334155", activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
    command=mostrar_lista_mascotas
).pack(fill="x", pady=5, ipady=8)

tk.Button(
    frame_menu, text="➕  Agregar Mascota", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white",
    activebackground="#334155", activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
    command=mostrar_formulario
).pack(fill="x", pady=5, ipady=8)

tk.Button(
    frame_menu, text="📅  Mis Reservas", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white",
    activebackground="#334155", activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
    command=mostrar_lista_reservas
).pack(fill="x", pady=5, ipady=8)

tk.Button(
    frame_menu, text="💉  Historial y Vacunas", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white",
    activebackground="#334155", activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
    command=mostrar_lista_historial
).pack(fill="x", pady=5, ipady=8)

frame_contenido = tk.Frame(ventana, bg=COLOR_BG_MAIN)
frame_contenido.pack(side="right", fill="both", expand=True)

mostrar_lista_mascotas()

ventana.mainloop()
