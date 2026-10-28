import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
from configuracion.base_datos import inicializar_base_datos, obtener_conexion
from controladores.mascota_controlador import MascotaControlador
from controladores.reserva_controlador import ReservaControlador
from controladores.historial_controlador import HistorialControlador

# Inicializar base de datos
inicializar_base_datos()

# CONSTANTES Y ESTILOS
COLOR_BG_MAIN = "#F8FAFC"
COLOR_SIDEBAR = "#1E293B"
COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_HOVER = "#1D4ED8"
COLOR_CARD_BG = "#FFFFFF"
COLOR_TEXT = "#0F172A"
COLOR_MUTED = "#64748B"
COLOR_DANGER = "#EF4444"
COLOR_SUCCESS = "#10B981"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

usuario_actual = None

# ============================================================
# SISTEMA DE AUTENTICACIÓN Y REGISTRO DE ROLES
# ============================================================

def registrar_nuevo_usuario(nombre, username, password, rol="Cliente"):
    if not nombre.strip() or not username.strip() or not password.strip() or not rol:
        return False, "Todos los campos son obligatorios."
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, username, password, rol)
            VALUES (?, ?, ?, ?)
        """, (nombre.strip(), username.strip(), password.strip(), rol))
        conexion.commit()
        conexion.close()
        return True, f"¡Cuenta de [{rol}] creada exitosamente!"
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe. Elige otro."
    except Exception as e:
        return False, f"Error al registrar: {str(e)}"

def iniciar_sesion():
    global usuario_actual
    user = entrada_user.get().strip()
    pwd = entrada_pass.get().strip()

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre, rol FROM usuarios WHERE username = ? AND password = ?", (user, pwd))
    fila = cursor.fetchone()
    conexion.close()

    if fila:
        usuario_actual = {"id_usuario": fila[0], "nombre": fila[1], "rol": fila[2]}
        frame_login.pack_forget()
        construir_interfaz_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def cerrar_sesion():
    global usuario_actual
    usuario_actual = None
    for widget in ventana.winfo_children():
        widget.destroy()
    mostrar_pantalla_login()

def mostrar_pantalla_login():
    for widget in ventana.winfo_children():
        widget.destroy()

    global frame_login, entrada_user, entrada_pass
    frame_login = tk.Frame(ventana, bg=COLOR_BG_MAIN)
    frame_login.pack(fill="both", expand=True)

    box = tk.Frame(frame_login, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=40, pady=35)
    box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(box, text="🐾 Veterinaria", font=("Segoe UI", 22, "bold"), bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(pady=(0, 20))
    
    tk.Label(box, text="Usuario:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    entrada_user = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid", width=30)
    entrada_user.pack(pady=(2, 10), ipady=4)

    tk.Label(box, text="Contraseña:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    entrada_pass = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid", show="*", width=30)
    entrada_pass.pack(pady=(2, 15), ipady=4)

    tk.Button(box, text="Iniciar Sesión", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, cursor="hand2", command=iniciar_sesion, pady=8).pack(fill="x")
    tk.Button(box, text="Crear cuenta de Cliente 📝", font=FONT_BODY, bg="#E2E8F0", fg=COLOR_TEXT, bd=0, cursor="hand2", command=mostrar_pantalla_registro_cliente, pady=6).pack(fill="x", pady=(10, 0))

def mostrar_pantalla_registro_cliente():
    """Registro público restringido únicamente a usuarios tipo Cliente."""
    for widget in ventana.winfo_children():
        widget.destroy()

    frame_reg = tk.Frame(ventana, bg=COLOR_BG_MAIN)
    frame_reg.pack(fill="both", expand=True)

    box = tk.Frame(frame_reg, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=40, pady=30)
    box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(box, text="📝 Registro de Cliente", font=("Segoe UI", 18, "bold"), bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(pady=(0, 15))

    tk.Label(box, text="Nombre completo:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_nombre = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid", width=32)
    e_nombre.pack(pady=(2, 10), ipady=4)

    tk.Label(box, text="Nombre de usuario (Login):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_user = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid", width=32)
    e_user.pack(pady=(2, 10), ipady=4)

    tk.Label(box, text="Contraseña:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_pass = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid", show="*", width=32)
    e_pass.pack(pady=(2, 15), ipady=4)

    def guardar_cliente():
        exito, msg = registrar_nuevo_usuario(e_nombre.get(), e_user.get(), e_pass.get(), "Cliente")
        if exito:
            messagebox.showinfo("¡Éxito!", msg)
            mostrar_pantalla_login()
        else:
            messagebox.showerror("Atención", msg)

    tk.Button(box, text="Registrarme como Cliente", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, cursor="hand2", command=guardar_cliente, pady=8).pack(fill="x", pady=(5, 8))
    tk.Button(box, text="Volver al Inicio de Sesión", font=FONT_BODY, bg="#64748B", fg="white", bd=0, cursor="hand2", command=mostrar_pantalla_login, pady=6).pack(fill="x")

def construir_interfaz_principal():
    global frame_menu, frame_contenido

    frame_menu = tk.Frame(ventana, width=230, bg=COLOR_SIDEBAR)
    frame_menu.pack(side="left", fill="y")
    frame_menu.pack_propagate(False)

    tk.Label(frame_menu, text="VETERINARIA", font=("Segoe UI", 16, "bold"), bg=COLOR_SIDEBAR, fg="white").pack(pady=(30, 5))
    tk.Label(frame_menu, text=f"👤 {usuario_actual['nombre']}\n[{usuario_actual['rol']}]", font=FONT_BODY, bg=COLOR_SIDEBAR, fg="#94A3B8").pack(pady=(0, 20))

    if usuario_actual["rol"] == "Cliente":
        tk.Button(frame_menu, text="🐾 Mis Mascotas", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white", bd=0, anchor="w", padx=25, command=vista_mis_mascotas).pack(fill="x", ipady=8)
        tk.Button(frame_menu, text="➕ Agregar Mascota", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white", bd=0, anchor="w", padx=25, command=vista_agregar_mascota).pack(fill="x", ipady=8)
        tk.Button(frame_menu, text="📅 Mis Citas", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white", bd=0, anchor="w", padx=25, command=vista_mis_reservas).pack(fill="x", ipady=8)

    elif usuario_actual["rol"] == "Admin":
        tk.Button(frame_menu, text="⚙️ Panel Admin General", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white", bd=0, anchor="w", padx=25, command=vista_admin_panel).pack(fill="x", ipady=8)

    else: # Veterinario, Cuidador, Estilista
        tk.Button(frame_menu, text=f"📅 Agenda [{usuario_actual['rol']}]", font=FONT_BOLD, bg=COLOR_SIDEBAR, fg="white", bd=0, anchor="w", padx=25, command=vista_empleado_reservas).pack(fill="x", ipady=8)

    tk.Button(frame_menu, text="🚪 Cerrar Sesión", font=FONT_BOLD, bg="#991B1B", fg="white", bd=0, anchor="w", padx=25, command=cerrar_sesion).pack(side="bottom", fill="x", ipady=8)

    frame_contenido = tk.Frame(ventana, bg=COLOR_BG_MAIN)
    frame_contenido.pack(side="right", fill="both", expand=True)

    if usuario_actual["rol"] == "Cliente":
        vista_mis_mascotas()
    elif usuario_actual["rol"] == "Admin":
        vista_admin_panel()
    else:
        vista_empleado_reservas()

def limpiar_contenido():
    for widget in frame_contenido.winfo_children():
        widget.destroy()

# ============================================================
# MODALES PARA HISTORIAL MÉDICO Y EDICIÓN
# ============================================================

def abrir_ventana_agregar_historial(id_mascota):
    top = tk.Toplevel(ventana)
    top.title("💉 Agregar Registro Médico")
    top.geometry("420x450")
    top.configure(bg=COLOR_CARD_BG)
    top.grab_set()

    tk.Label(top, text="🩺 Nuevo Registro en Historia Clínica", font=FONT_SUBTITLE, bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(pady=15)

    tk.Label(top, text="Tipo de Registro:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25)
    c_tipo = ttk.Combobox(top, values=["Consulta", "Vacuna", "Desparasitación", "Examen"], state="readonly", font=FONT_BODY)
    c_tipo.set("Consulta")
    c_tipo.pack(fill="x", padx=25, pady=2)

    tk.Label(top, text="Descripción / Diagnóstico:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25, pady=(8, 0))
    e_desc = tk.Text(top, font=FONT_BODY, height=3, bd=1, relief="solid")
    e_desc.pack(fill="x", padx=25, pady=2)

    tk.Label(top, text="Fecha Aplicación (YYYY-MM-DD):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25, pady=(8, 0))
    e_fecha = tk.Entry(top, font=FONT_BODY, bd=1, relief="solid")
    e_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
    e_fecha.pack(fill="x", padx=25, pady=2)

    tk.Label(top, text="Próxima Dosis / Control (Opcional):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25, pady=(8, 0))
    e_prox = tk.Entry(top, font=FONT_BODY, bd=1, relief="solid")
    e_prox.pack(fill="x", padx=25, pady=2)

    def guardar():
        exito, res = HistorialControlador.registrar_historial(
            id_mascota, c_tipo.get(), e_desc.get("1.0", tk.END).strip(), e_fecha.get().strip(), e_prox.get().strip()
        )
        if exito:
            messagebox.showinfo("Éxito", res, parent=top)
            top.destroy()
            vista_perfil_mascota(id_mascota)
        else:
            messagebox.showerror("Error", "\n".join(res), parent=top)

    tk.Button(top, text="💾 Guardar en Historial", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=guardar, pady=8).pack(fill="x", padx=25, pady=20)


def abrir_ventana_editar_mascota(id_mascota):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT peso, observaciones FROM mascotas WHERE id_mascota = ?", (id_mascota,))
    fila = cursor.fetchone()
    conexion.close()

    if not fila:
        return

    top = tk.Toplevel(ventana)
    top.title("✏️ Editar Perfil de Mascota")
    top.geometry("420x330")
    top.configure(bg=COLOR_CARD_BG)
    top.grab_set()

    tk.Label(top, text="✏️ Actualizar Datos Físicos y Clínicos", font=FONT_SUBTITLE, bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(pady=15)

    tk.Label(top, text="Peso Actual (kg):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25)
    e_peso = tk.Entry(top, font=FONT_BODY, bd=1, relief="solid")
    e_peso.insert(0, str(fila[0]))
    e_peso.pack(fill="x", padx=25, pady=2)

    tk.Label(top, text="Observaciones / Alergias del Paciente:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", padx=25, pady=(8, 0))
    e_obs = tk.Text(top, font=FONT_BODY, height=3, bd=1, relief="solid")
    e_obs.insert("1.0", fila[1] or "")
    e_obs.pack(fill="x", padx=25, pady=2)

    def actualizar():
        try:
            nuevo_peso = float(e_peso.get().strip())
            nuevas_obs = e_obs.get("1.0", tk.END).strip()
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("UPDATE mascotas SET peso = ?, observaciones = ? WHERE id_mascota = ?", (nuevo_peso, nuevas_obs, id_mascota))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Perfil de la mascota actualizado.", parent=top)
            top.destroy()
            vista_perfil_mascota(id_mascota)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número válido.", parent=top)

    tk.Button(top, text="💾 Guardar Cambios", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=actualizar, pady=8).pack(fill="x", padx=25, pady=20)

# ============================================================
# VISTAS
# ============================================================

def vista_mis_mascotas():
    limpiar_contenido()
    mascotas = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])

    tk.Label(frame_contenido, text="🐾 Mis Mascotas", font=FONT_TITLE, bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(anchor="w", padx=30, pady=20)

    for m in mascotas:
        card = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=10)
        card.pack(fill="x", padx=30, pady=5)

        icono, desc_sem, col = MascotaControlador.calcular_semaforo_vacunacion(m["id_mascota"])

        info = f"{m['nombre']} ({m['tipo']}) - {m['raza']} | ⏳ {m['edad_meses']} meses | ⚖️ {m['peso']} kg"
        tk.Label(card, text=info, font=FONT_BOLD, bg=COLOR_CARD_BG).pack(side="left")
        
        tk.Label(card, text=f"Vacunas: {icono}", font=FONT_BOLD, fg=col, bg=COLOR_CARD_BG).pack(side="left", padx=15)

        tk.Button(card, text="Perfil 📋", font=FONT_BODY, bg=COLOR_PRIMARY, fg="white", bd=0, command=lambda id_m=m["id_mascota"]: vista_perfil_mascota(id_m)).pack(side="right", padx=2)
        tk.Button(card, text="Eliminar 🗑️", font=FONT_BODY, bg=COLOR_DANGER, fg="white", bd=0, command=lambda id_m=m["id_mascota"]: accion_eliminar_mascota(id_m)).pack(side="right", padx=2)


def vista_perfil_mascota(id_mascota):
    limpiar_contenido()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT m.nombre, m.tipo, m.raza, m.edad_meses, m.peso, m.observaciones, u.nombre 
        FROM mascotas m 
        JOIN usuarios u ON m.id_usuario = u.id_usuario 
        WHERE m.id_mascota = ?
    """, (id_mascota,))
    m = cursor.fetchone()
    conexion.close()

    if not m:
        return

    top_bar = tk.Frame(frame_contenido, bg=COLOR_BG_MAIN)
    top_bar.pack(fill="x", padx=30, pady=15)

    tk.Label(top_bar, text=f"📋 Perfil de {m[0]}", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(side="left")

    if usuario_actual["rol"] in ["Veterinario", "Admin"]:
        tk.Button(top_bar, text="➕ Vacuna / Consulta 💉", font=FONT_BOLD, bg=COLOR_SUCCESS, fg="white", bd=0, command=lambda: abrir_ventana_agregar_historial(id_mascota), padx=10, pady=5).pack(side="right", padx=5)
        tk.Button(top_bar, text="✏️ Editar Peso/Notas", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=lambda: abrir_ventana_editar_mascota(id_mascota), padx=10, pady=5).pack(side="right", padx=5)

    card = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=25, pady=20)
    card.pack(fill="x", padx=30, pady=5)

    icono, desc, col = MascotaControlador.calcular_semaforo_vacunacion(id_mascota)
    tk.Label(card, text=f"Semáforo de Vacunación: {icono} {desc}", font=FONT_BOLD, fg=col, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 10))

    details = f"• Dueño: {m[6]}\n• Tipo: {m[1]} | Raza: {m[2]}\n• Edad: {m[3]} meses | Peso: {m[4]} kg\n• Observaciones Médicas: {m[5] or 'Sin observaciones.'}"
    tk.Label(card, text=details, font=FONT_BODY, bg=COLOR_CARD_BG, justify="left").pack(anchor="w")

    tk.Label(frame_contenido, text="💉 Historial Médico y Diagnósticos", font=FONT_SUBTITLE, bg=COLOR_BG_MAIN).pack(anchor="w", padx=30, pady=(15, 5))
    historiales = HistorialControlador.obtener_historial_por_mascota(id_mascota)

    if not historiales:
        tk.Label(frame_contenido, text="Sin registros en el historial médico aún.", font=FONT_BODY, bg=COLOR_BG_MAIN, fg=COLOR_MUTED).pack(anchor="w", padx=30)
    else:
        for h in historiales:
            h_card = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=10, pady=5)
            h_card.pack(fill="x", padx=30, pady=2)
            tk.Label(h_card, text=f"[{h['fecha']}] {h['tipo_registro']}: {h['descripcion']} (Próx: {h['proxima_dosis'] or 'N/A'})", font=FONT_BODY, bg=COLOR_CARD_BG).pack(anchor="w")

    def volver():
        if usuario_actual["rol"] == "Admin":
            vista_admin_panel()
        elif usuario_actual["rol"] in ["Veterinario", "Cuidador", "Estilista"]:
            vista_empleado_reservas()
        else:
            vista_mis_mascotas()

    tk.Button(frame_contenido, text="⬅️ Volver", font=FONT_BOLD, bg="#64748B", fg="white", bd=0, command=volver, padx=15, pady=5).pack(pady=15)


def vista_agregar_mascota():
    limpiar_contenido()
    tk.Label(frame_contenido, text="➕ Agregar Nueva Mascota", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(pady=20)

    box = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=30, pady=20)
    box.pack(padx=60, fill="x")

    def f_campo(lbl):
        tk.Label(box, text=lbl, font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
        e = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid")
        e.pack(fill="x", ipady=3)
        return e

    e_nom = f_campo("Nombre:")
    tk.Label(box, text="Tipo:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
    c_tipo = ttk.Combobox(box, values=["Perro 🐶", "Gato 🐱", "Ave 🦜", "Otro 🐾"], state="readonly")
    c_tipo.pack(fill="x")

    e_raza = f_campo("Raza:")
    e_edad = f_campo("Edad (en Meses):")
    e_peso = f_campo("Peso (kg):")
    e_obs = f_campo("Observaciones:")

    def guardar():
        exito, res = MascotaControlador.registrar_mascota(
            usuario_actual["id_usuario"], e_nom.get(), c_tipo.get(), e_raza.get(), e_edad.get(), e_peso.get(), e_obs.get()
        )
        if exito:
            messagebox.showinfo("Éxito", res)
            vista_mis_mascotas()
        else:
            messagebox.showerror("Error", "\n".join(res))

    tk.Button(box, text="Guardar Mascota", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=guardar, pady=8).pack(fill="x", pady=20)


def accion_eliminar_mascota(id_mascota):
    if messagebox.askyesno("Confirmar", "¿Eliminar la mascota y todo su historial?"):
        exito, msg = MascotaControlador.eliminar_mascota(id_mascota)
        if exito:
            messagebox.showinfo("Éxito", msg)
            if usuario_actual["rol"] == "Admin":
                vista_admin_panel()
            else:
                vista_mis_mascotas()
        else:
            messagebox.showerror("Error", msg)


def vista_mis_reservas():
    limpiar_contenido()
    tk.Label(frame_contenido, text="📅 Mis Citas Agendadas", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(anchor="w", padx=30, pady=20)

    tk.Button(frame_contenido, text="➕ Agendar Nueva Cita / Guardería", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=vista_agendar_cita).pack(anchor="w", padx=30, pady=(0, 15))

    reservas = ReservaControlador.obtener_reservas_por_usuario(usuario_actual["id_usuario"])

    for r in reservas:
        card = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=10)
        card.pack(fill="x", padx=30, pady=5)

        info = f"🐾 {r['nombre_mascota']} | {r['servicio']} ({r['rol_encargado']}) - Estado: {r['estado']}\n🕒 Fecha: {r['fecha_reserva']}"
        if r['servicio'] == "Guardería 🏡" and r['fecha_fin']:
            info += f"  ➔  Fin: {r['fecha_fin']}"
        info += f" | 💵 ${r['costo_estimado']}"

        tk.Label(card, text=info, font=FONT_BOLD, bg=COLOR_CARD_BG, justify="left").pack(side="left")

        tk.Button(card, text="Eliminar 🗑️", font=FONT_BODY, bg=COLOR_DANGER, fg="white", bd=0, command=lambda id_r=r["id_reserva"]: accion_eliminar_cita(id_r)).pack(side="right")


def vista_agendar_cita():
    limpiar_contenido()
    tk.Label(frame_contenido, text="📅 Agendar Cita o Guardería", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(pady=10)

    mascotas = MascotaControlador.listar_mascotas_usuario(usuario_actual["id_usuario"])
    if not mascotas:
        messagebox.showwarning("Aviso", "Primero debes registrar una mascota.")
        vista_agregar_mascota()
        return

    box = tk.Frame(frame_contenido, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=30, pady=15)
    box.pack(padx=60, fill="x")

    dict_mascotas = {f"{m['nombre']} ({m['tipo']} - {m['raza']}, {m['peso']}kg)": m for m in mascotas}

    tk.Label(box, text="Selecciona Mascota:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    cb_mascota = ttk.Combobox(box, values=list(dict_mascotas.keys()), state="readonly")
    cb_mascota.pack(fill="x", pady=2)

    tk.Label(box, text="Servicio Requerido:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
    cb_servicio = ttk.Combobox(box, values=list(ReservaControlador.MAPA_ROLES.keys()), state="readonly")
    cb_servicio.pack(fill="x", pady=2)

    manana_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 09:00")

    tk.Label(box, text="Fecha y Hora (Mínimo a partir de mañana: YYYY-MM-DD HH:MM):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
    e_fecha = tk.Entry(box, font=FONT_BODY, bd=1, relief="solid")
    e_fecha.insert(0, manana_str)
    e_fecha.pack(fill="x", ipady=3)

    frame_guarderia = tk.Frame(box, bg=COLOR_CARD_BG)

    tk.Label(frame_guarderia, text="Fecha y Hora de Fin de Guardería (YYYY-MM-DD HH:MM):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
    manana_fin_str = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d 18:00")
    e_fecha_fin = tk.Entry(frame_guarderia, font=FONT_BODY, bd=1, relief="solid")
    e_fecha_fin.insert(0, manana_fin_str)
    e_fecha_fin.pack(fill="x", ipady=3)

    tk.Label(frame_guarderia, text="Observaciones de Cuidado / Indicaciones de Alimentación:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(8, 0))
    txt_obs_servicio = tk.Text(frame_guarderia, font=FONT_BODY, height=3, bd=1, relief="solid")
    txt_obs_servicio.pack(fill="x", pady=2)

    lbl_costo_var = tk.StringVar(value="Costo Estimado Automático: $0.0")
    tk.Label(box, textvariable=lbl_costo_var, font=("Segoe UI", 11, "bold"), fg=COLOR_PRIMARY, bg=COLOR_CARD_BG).pack(pady=10)

    def evento_cambio_servicio(event=None):
        if cb_servicio.get() == "Guardería 🏡":
            frame_guarderia.pack(fill="x", pady=5)
        else:
            frame_guarderia.pack_forget()

        if cb_mascota.get() and cb_servicio.get():
            m_obj = dict_mascotas[cb_mascota.get()]
            costo = ReservaControlador.calcular_costo_automatico(cb_servicio.get(), m_obj["peso"], m_obj["raza"])
            lbl_costo_var.set(f"Costo Estimado Automático (Peso + Raza): ${costo:,.2f}")

    cb_mascota.bind("<<ComboboxSelected>>", evento_cambio_servicio)
    cb_servicio.bind("<<ComboboxSelected>>", evento_cambio_servicio)

    def guardar_cita():
        if not cb_mascota.get() or not cb_servicio.get() or not e_fecha.get():
            messagebox.showerror("Error", "Completa todos los campos obligatorios.")
            return

        m_obj = dict_mascotas[cb_mascota.get()]
        costo = ReservaControlador.calcular_costo_automatico(cb_servicio.get(), m_obj["peso"], m_obj["raza"])

        f_fin = e_fecha_fin.get().strip() if cb_servicio.get() == "Guardería 🏡" else ""
        obs_serv = txt_obs_servicio.get("1.0", tk.END).strip() if cb_servicio.get() == "Guardería 🏡" else ""

        exito, msg = ReservaControlador.registrar_reserva(
            m_obj["id_mascota"], cb_servicio.get(), e_fecha.get().strip(), costo, f_fin, obs_serv
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            vista_mis_reservas()
        else:
            messagebox.showerror("Atención", msg)

    tk.Button(box, text="Confirmar Reserva", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=guardar_cita, pady=8).pack(fill="x", pady=10)


def accion_eliminar_cita(id_reserva):
    if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta cita?"):
        exito, msg = ReservaControlador.eliminar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", msg)
            if usuario_actual["rol"] == "Admin":
                vista_admin_panel()
            elif usuario_actual["rol"] == "Cliente":
                vista_mis_reservas()
            else:
                vista_empleado_reservas()


def accion_completar_cita(id_reserva):
    """Marca la cita como realizada para incluirla en las ganancias del día."""
    exito, msg = ReservaControlador.completar_reserva(id_reserva)
    if exito:
        messagebox.showinfo("¡Cita Finalizada!", msg)
        if usuario_actual["rol"] == "Admin":
            vista_admin_panel()
        else:
            vista_empleado_reservas()


def vista_empleado_reservas():
    limpiar_contenido()
    rol = usuario_actual["rol"]
    tk.Label(frame_contenido, text=f"📋 Agenda de Citas Organizada por Día [{rol}]", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(anchor="w", padx=30, pady=15)

    reservas = ReservaControlador.obtener_reservas_por_rol(rol)

    if not reservas:
        tk.Label(frame_contenido, text=f"No hay citas asignadas para el rol de {rol}.", font=FONT_BODY, bg=COLOR_BG_MAIN, fg=COLOR_MUTED).pack(anchor="w", padx=30)
        return

    agrupadas_por_dia = {}
    for r in reservas:
        dia = r["fecha_reserva"].split(" ")[0]
        if dia not in agrupadas_por_dia:
            agrupadas_por_dia[dia] = []
        agrupadas_por_dia[dia].append(r)

    for dia in sorted(agrupadas_por_dia.keys()):
        frame_dia = tk.LabelFrame(frame_contenido, text=f" 📅 Día: {dia} ", font=FONT_SUBTITLE, bg=COLOR_BG_MAIN, fg=COLOR_PRIMARY, padx=10, pady=10)
        frame_dia.pack(fill="x", padx=30, pady=8)

        for r in agrupadas_por_dia[dia]:
            card = tk.Frame(frame_dia, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=8)
            card.pack(fill="x", pady=4)

            info = f"🕒 Hora: {r['fecha_reserva'].split(' ')[-1]} | {r['servicio']} | Estado: {r['estado']}\n🐾 Paciente: {r['nombre_mascota']} | 👤 Dueño: {r['dueno']}"
            if r['servicio'] == "Guardería 🏡":
                info += f"\n🗓️ Cuidados del {r['fecha_reserva']} al {r['fecha_fin']}\n🥣 Alimentación/Notas: {r['observaciones_servicio'] or 'Sin notas'}"

            tk.Label(card, text=info, font=FONT_BOLD, bg=COLOR_CARD_BG, justify="left").pack(side="left")

            tk.Button(card, text="Ver Perfil 📋", font=FONT_BODY, bg=COLOR_PRIMARY, fg="white", bd=0, command=lambda id_m=r["id_mascota"]: vista_perfil_mascota(id_m)).pack(side="right", padx=2)
            
            if r['estado'] != "Realizada":
                tk.Button(card, text="Marcar Realizada ✅", font=FONT_BODY, bg=COLOR_SUCCESS, fg="white", bd=0, command=lambda id_r=r["id_reserva"]: accion_completar_cita(id_r)).pack(side="right", padx=2)


# ============================================================
# PANEL DE CONTROL GENERAL DE ADMINISTRADOR
# ============================================================

def vista_admin_panel():
    limpiar_contenido()

    tk.Label(frame_contenido, text="⚙️ Panel General de Administración", font=FONT_TITLE, bg=COLOR_BG_MAIN).pack(anchor="w", padx=30, pady=15)

    notebook = ttk.Notebook(frame_contenido)
    notebook.pack(fill="both", expand=True, padx=30, pady=10)

    # 1. PESTAÑA MASCOTAS
    tab_mascotas = tk.Frame(notebook, bg=COLOR_BG_MAIN)
    notebook.add(tab_mascotas, text="🐾 Todas las Mascotas")

    search_frame = tk.Frame(tab_mascotas, bg=COLOR_BG_MAIN)
    search_frame.pack(fill="x", padx=15, pady=10)

    e_busqueda = tk.Entry(search_frame, font=FONT_BODY, bd=1, relief="solid")
    e_busqueda.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 10))

    cont_res = tk.Frame(tab_mascotas, bg=COLOR_BG_MAIN)
    cont_res.pack(fill="both", expand=True, padx=15, pady=5)

    def ejecutar_busqueda():
        for w in cont_res.winfo_children():
            w.destroy()
        res = MascotaControlador.buscar_mascotas_admin(e_busqueda.get())
        for m in res:
            card = tk.Frame(cont_res, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=8)
            card.pack(fill="x", pady=4)
            icono, _, col = MascotaControlador.calcular_semaforo_vacunacion(m["id_mascota"])
            info = f"🐶 {m['nombre']} ({m['tipo']} - {m['raza']}) | 👤 Dueño: {m['dueno']} | ⚖️ {m['peso']} kg"
            tk.Label(card, text=info, font=FONT_BOLD, bg=COLOR_CARD_BG).pack(side="left")
            tk.Label(card, text=f"Vacunas: {icono}", font=FONT_BOLD, fg=col, bg=COLOR_CARD_BG).pack(side="left", padx=10)
            tk.Button(card, text="Ver Perfil 📋", font=FONT_BODY, bg=COLOR_PRIMARY, fg="white", bd=0, command=lambda id_m=m["id_mascota"]: vista_perfil_mascota(id_m)).pack(side="right", padx=2)
            tk.Button(card, text="Eliminar 🗑️", font=FONT_BODY, bg=COLOR_DANGER, fg="white", bd=0, command=lambda id_m=m["id_mascota"]: accion_eliminar_mascota(id_m)).pack(side="right", padx=2)

    tk.Button(search_frame, text="Buscar", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=ejecutar_busqueda, padx=15).pack(side="right")
    ejecutar_busqueda()

    # 2. PESTAÑA CITAS POR ROL DE SERVICIO
    tab_citas = tk.Frame(notebook, bg=COLOR_BG_MAIN)
    notebook.add(tab_citas, text="📅 Citas por Rol")

    notebook_roles = ttk.Notebook(tab_citas)
    notebook_roles.pack(fill="both", expand=True, padx=10, pady=10)

    roles_lista = [
        ("🩺 Servicio Veterinario", "Veterinario"),
        ("✂️ Servicio Estilista", "Estilista"),
        ("🏡 Servicio Cuidador", "Cuidador")
    ]

    todas_citas = ReservaControlador.obtener_reservas_por_rol("Admin")

    for titulo_tab, nombre_rol in roles_lista:
        tab_rol = tk.Frame(notebook_roles, bg=COLOR_BG_MAIN)
        notebook_roles.add(tab_rol, text=titulo_tab)

        citas_rol = [c for c in todas_citas if c["rol_encargado"] == nombre_rol]

        if not citas_rol:
            tk.Label(tab_rol, text=f"Sin citas para {nombre_rol}.", font=FONT_BODY, bg=COLOR_BG_MAIN, fg=COLOR_MUTED).pack(pady=30)
        else:
            for c in citas_rol:
                card_c = tk.Frame(tab_rol, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=8)
                card_c.pack(fill="x", padx=15, pady=4)

                detalles = f"🕒 {c['fecha_reserva']} | {c['servicio']} | Estado: {c['estado']}\n🐾 Mascota: {c['nombre_mascota']} | 👤 Dueño: {c['dueno']} | 💵 Costo: ${c['costo_estimado']}"
                if c['servicio'] == "Guardería 🏡":
                    detalles += f"\n🗓️ Hasta: {c['fecha_fin']} | 🥣 Comida/Notas: {c['observaciones_servicio']}"

                tk.Label(card_c, text=detalles, font=FONT_BOLD, bg=COLOR_CARD_BG, justify="left").pack(side="left")

                tk.Button(card_c, text="Ver Perfil 📋", font=FONT_BODY, bg=COLOR_PRIMARY, fg="white", bd=0, command=lambda id_m=c["id_mascota"]: vista_perfil_mascota(id_m)).pack(side="right", padx=2)
                
                if c['estado'] != "Realizada":
                    tk.Button(card_c, text="Marcar Realizada ✅", font=FONT_BODY, bg=COLOR_SUCCESS, fg="white", bd=0, command=lambda id_r=c["id_reserva"]: accion_completar_cita(id_r)).pack(side="right", padx=2)

                tk.Button(card_c, text="Eliminar 🗑️", font=FONT_BODY, bg=COLOR_DANGER, fg="white", bd=0, command=lambda id_r=c["id_reserva"]: accion_eliminar_cita(id_r)).pack(side="right", padx=2)

    # 3. PESTAÑA CREAR EMPLEADOS / ROLES (Exclusivo Administrador)
    tab_crear_emp = tk.Frame(notebook, bg=COLOR_BG_MAIN)
    notebook.add(tab_crear_emp, text="👥 Registrar Personal")

    box_emp = tk.Frame(tab_crear_emp, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=30, pady=20)
    box_emp.pack(padx=60, pady=20, fill="x")

    tk.Label(box_emp, text="➕ Registrar Nuevo Empleado o Administrador", font=FONT_SUBTITLE, bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(pady=(0, 10))

    tk.Label(box_emp, text="Nombre Completo:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_emp_nom = tk.Entry(box_emp, font=FONT_BODY, bd=1, relief="solid")
    e_emp_nom.pack(fill="x", ipady=3, pady=(0, 8))

    tk.Label(box_emp, text="Nombre de Usuario (Login):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_emp_user = tk.Entry(box_emp, font=FONT_BODY, bd=1, relief="solid")
    e_emp_user.pack(fill="x", ipady=3, pady=(0, 8))

    tk.Label(box_emp, text="Contraseña:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    e_emp_pass = tk.Entry(box_emp, font=FONT_BODY, bd=1, relief="solid", show="*")
    e_emp_pass.pack(fill="x", ipady=3, pady=(0, 8))

    tk.Label(box_emp, text="Rol del Empleado:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
    cb_emp_rol = ttk.Combobox(box_emp, values=["Admin", "Veterinario", "Cuidador", "Estilista"], state="readonly", font=FONT_BODY)
    cb_emp_rol.set("Veterinario")
    cb_emp_rol.pack(fill="x", pady=(0, 15))

    def guardar_empleado():
        exito, msg = registrar_nuevo_usuario(e_emp_nom.get(), e_emp_user.get(), e_emp_pass.get(), cb_emp_rol.get())
        if exito:
            messagebox.showinfo("Éxito", msg)
            e_emp_nom.delete(0, tk.END)
            e_emp_user.delete(0, tk.END)
            e_emp_pass.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    tk.Button(box_emp, text="Crear Usuario de Personal", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white", bd=0, command=guardar_empleado, pady=8).pack(fill="x")

    # 4. PESTAÑA DE BALANCE DIARIO Y CITAS REALIZADAS
    tab_balance = tk.Frame(notebook, bg=COLOR_BG_MAIN)
    notebook.add(tab_balance, text="💰 Control Diario y Ganancias")

    frame_filtro = tk.Frame(tab_balance, bg=COLOR_BG_MAIN)
    frame_filtro.pack(fill="x", padx=15, pady=10)

    tk.Label(frame_filtro, text="Seleccionar Fecha (YYYY-MM-DD):", font=FONT_BOLD, bg=COLOR_BG_MAIN).pack(side="left", padx=(0, 5))
    e_fecha_bal = tk.Entry(frame_filtro, font=FONT_BODY, bd=1, relief="solid", width=15)
    e_fecha_bal.insert(0, datetime.now().strftime("%Y-%m-%d"))
    e_fecha_bal.pack(side="left", ipady=3, padx=(0, 10))

    cont_balance_res = tk.Frame(tab_balance, bg=COLOR_BG_MAIN)
    cont_balance_res.pack(fill="both", expand=True, padx=15, pady=5)

    lbl_total_ganado = tk.Label(tab_balance, text="Total Ganado Hoy: $0.00", font=("Segoe UI", 14, "bold"), fg=COLOR_SUCCESS, bg=COLOR_BG_MAIN)
    lbl_total_ganado.pack(pady=10)

    def calcular_balance():
        for w in cont_balance_res.winfo_children():
            w.destroy()

        fecha_sel = e_fecha_bal.get().strip()
        citas_realizadas, total = ReservaControlador.obtener_cierre_diario(fecha_sel)

        lbl_total_ganado.config(text=f"Total Recaudado el {fecha_sel}: ${total:,.2f}")

        if not citas_realizadas:
            tk.Label(cont_balance_res, text=f"No hay citas marcadas como REALIZADAS en la fecha {fecha_sel}.", font=FONT_BODY, bg=COLOR_BG_MAIN, fg=COLOR_MUTED).pack(pady=20)
            return

        for c in citas_realizadas:
            card = tk.Frame(cont_balance_res, bg=COLOR_CARD_BG, bd=1, relief="solid", padx=15, pady=8)
            card.pack(fill="x", pady=4)
            info = f"✅ [{c['fecha_reserva'].split(' ')[-1]}] {c['servicio']} ({c['rol_encargado']})\n🐾 Mascota: {c['nombre_mascota']} | 👤 Dueño: {c['dueno']} | 💵 Cobrado: ${c['costo_estimado']:,.2f}"
            tk.Label(card, text=info, font=FONT_BOLD, bg=COLOR_CARD_BG, justify="left").pack(side="left")

    tk.Button(frame_filtro, text="Calcular Cierre del Día 📊", font=FONT_BOLD, bg=COLOR_SUCCESS, fg="white", bd=0, command=calcular_balance, padx=15).pack(side="left")
    calcular_balance()


# ============================================================
# INICIALIZACIÓN Y EJECUCIÓN
# ============================================================
ventana = tk.Tk()
ventana.title("Sistema Veterinario")
ventana.geometry("950x700")
ventana.configure(bg=COLOR_BG_MAIN)

mostrar_pantalla_login()

ventana.mainloop()