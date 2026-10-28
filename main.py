import tkinter as tk
from tkinter import messagebox
from configuracion.base_datos import inicializar_base_datos, obtener_conexion
from controladores.mascotas_controlador import MascotaControlador
from controladores.reserva_controlador import ReservaControlador
from controladores.historial_controlador import HistorialControlador

# Inicializar base de datos local
inicializar_base_datos()

# Variables globales de sesión
usuario_actual = {"id_usuario": 1, "nombre": "Cesar David (Dueño)"}

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Mascotas - Veterinaria UAN")
        self.root.geometry("1024x640")
        self.root.minsize(900, 550)

        # Colores de la interfaz
        self.COLOR_SIDEBAR = "#1E293B"
        self.COLOR_BG_MAIN = "#F8FAFC"
        self.COLOR_PRIMARY = "#2563EB"
        self.COLOR_TEXT = "#0F172A"
        
        self.FONT_TITLE = ("Arial", 16, "bold")
        self.FONT_BOLD = ("Arial", 11, "bold")
        self.FONT_NORMAL = ("Arial", 11)

        self.construir_interfaz()

    def construir_interfaz(self):
        # Contenedor principal
        self.main_container = tk.Frame(self.root, bg=self.COLOR_BG_MAIN)
        self.main_container.pack(fill="both", expand=True)

        # Menú lateral (Sidebar)
        self.frame_menu = tk.Frame(self.main_container, bg=self.COLOR_SIDEBAR, width=240)
        self.frame_menu.pack(side="left", fill="y")
        self.frame_menu.pack_propagate(False)

        # Título en el menú
        lbl_titulo = tk.Label(self.frame_menu, text="VETERINARIA", font=("Arial", 14, "bold"), bg=self.COLOR_SIDEBAR, fg="white")
        lbl_titulo.pack(pady=(30, 10))

        self.lbl_usuario = tk.Label(self.frame_menu, text=f"Hola, {usuario_actual['nombre']}", font=("Arial", 9), bg=self.COLOR_SIDEBAR, fg="#94A3B8")
        self.lbl_usuario.pack(pady=(0, 30))

        # Opciones del menú
        self.crear_boton_menu("🐾  Mis Mascotas", self.mostrar_lista_mascotas)
        self.crear_boton_menu("➕  Registrar Mascota", self.mostrar_registro_mascota)
        self.crear_boton_menu("📅  Mis Reservas", self.mostrar_reservas)
        self.crear_boton_menu("🩺  Historial y Vacunas", self.mostrar_historial)

        # Botón de Cerrar Sesión (Punto 9)
        btn_salir = tk.Button(
            self.frame_menu, text="🚪  Cerrar Sesión", font=self.FONT_BOLD, bg="#DC2626", fg="white",
            activebackground="#B91C1C", activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
            command=self.cerrar_sesion
        )
        btn_salir.pack(side="bottom", fill="x", pady=20, ipady=8)

        # Área de contenido principal
        self.frame_contenido = tk.Frame(self.main_container, bg=self.COLOR_BG_MAIN)
        self.frame_contenido.pack(side="right", fill="both", expand=True)

        # Mostrar pantalla inicial
        self.mostrar_lista_mascotas()

    def crear_boton_menu(self, texto, comando):
        btn = tk.Button(
            self.frame_menu, text=texto, font=self.FONT_NORMAL, bg=self.COLOR_SIDEBAR, fg="#E2E8F0",
            activebackground=self.COLOR_PRIMARY, activeforeground="white", bd=0, anchor="w", padx=25, cursor="hand2",
            command=comando
        )
        btn.pack(fill="x", pady=5, ipady=6)

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_lista_mascotas(self):
        self.limpiar_contenido()
        
        lbl = tk.Label(self.frame_contenido, text="Mis Mascotas (Base de Datos)", font=self.FONT_TITLE, bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT)
        lbl.pack(anchor="w", padx=30, pady=20)

        mascotas = MascotaControlador.obtener_mascotas_por_usuario(usuario_actual["id_usuario"])

        if not mascotas:
            lbl_vacio = tk.Label(self.frame_contenido, text="No tienes mascotas registradas aún.", font=self.FONT_NORMAL, bg=self.COLOR_BG_MAIN, fg="#64748B")
            lbl_vacio.pack(padx=30, anchor="w", pady=10)
        else:
            for m in mascotas:
                # m = (id_mascota, id_usuario, nombre, tipo, raza, edad, peso, observaciones)
                frame_card = tk.Frame(self.frame_contenido, bg="white", bd=1, relief="solid")
                frame_card.pack(fill="x", padx=30, pady=6, ipady=8, ipadx=15)

                info_text = f"🐾 {m[2]}  |  Tipo: {m[3]}  |  Raza: {m[4]}  |  Edad: {m[5]} años  |  Peso: {m[6]} kg"
                tk.Label(frame_card, text=info_text, font=self.FONT_BOLD, bg="white", fg=self.COLOR_TEXT).pack(side="left", anchor="w")

                # Botón para eliminar mascota (Punto 10)
                btn_eliminar = tk.Button(
                    frame_card, text="Eliminar", bg="#EF4444", fg="white", font=("Arial", 9, "bold"),
                    bd=0, padx=10, pady=2, cursor="hand2",
                    command=lambda id_m=m[0]: self.eliminar_mascota_accion(id_m)
                )
                btn_eliminar.pack(side="right", padx=10)

        # Botón inferior para ir al registro
        btn_reg = tk.Button(
            self.frame_contenido, text="+ Registrar Nueva Mascota", font=self.FONT_BOLD, bg=self.COLOR_PRIMARY, fg="white",
            padx=15, pady=8, bd=0, cursor="hand2", command=self.mostrar_registro_mascota
        )
        btn_reg.pack(anchor="w", padx=30, pady=20)

    def eliminar_mascota_accion(self, id_mascota):
        if messagebox.askyesno("Eliminar Mascota", "¿Estás seguro de eliminar esta mascota?"):
            MascotaControlador.eliminar_mascota(id_mascota)
            messagebox.showinfo("Éxito", "Mascota eliminada correctamente.")
            self.mostrar_lista_mascotas()

    def mostrar_registro_mascota(self):
        self.limpiar_contenido()
        lbl = tk.Label(self.frame_contenido, text="Registrar Nueva Mascota", font=self.FONT_TITLE, bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT)
        lbl.pack(anchor="w", padx=30, pady=20)

        form_frame = tk.Frame(self.frame_contenido, bg=self.COLOR_BG_MAIN)
        form_frame.pack(anchor="w", padx=30)

        campos = [
            ("Nombre de la mascota:", "entry_nombre"),
            ("Tipo (Ej. Perro/Gato):", "entry_tipo"),
            ("Raza:", "entry_raza"),
            ("Edad (años):", "entry_edad"),
            ("Peso (kg):", "entry_peso"),
            ("Observaciones:", "entry_obs")
        ]

        entradas = {}
        for i, (label_text, key) in enumerate(campos):
            tk.Label(form_frame, text=label_text, font=self.FONT_NORMAL, bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT).grid(row=i, column=0, sticky="w", pady=6)
            entry = tk.Entry(form_frame, font=self.FONT_NORMAL, width=30)
            entry.grid(row=i, column=1, padx=15, pady=6)
            entradas[key] = entry

        def guardar():
            nombre = entradas["entry_nombre"].get().strip()
            tipo = entradas["entry_tipo"].get().strip()
            raza = entradas["entry_raza"].get().strip()
            edad = entradas["entry_edad"].get().strip()
            peso = entradas["entry_peso"].get().strip()
            obs = entradas["entry_obs"].get().strip()

            if not nombre or not tipo:
                messagebox.showerror("Error", "El nombre y el tipo son obligatorios.")
                return

            try:
                edad_val = float(edad) if edad else 0.0
                peso_val = float(peso) if peso else 0.0
                MascotaControlador.registrar_mascota(usuario_actual["id_usuario"], nombre, tipo, raza, edad_val, peso_val, obs)
                messagebox.showinfo("Éxito", "¡Mascota registrada exitosamente!")
                self.mostrar_lista_mascotas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar: {e}")

        btn_guardar = tk.Button(self.frame_contenido, text="Guardar Mascota", font=self.FONT_BOLD, bg=self.COLOR_PRIMARY, fg="white", padx=20, pady=8, bd=0, cursor="hand2", command=guardar)
        btn_guardar.pack(anchor="w", padx=30, pady=20)

    def mostrar_reservas(self):
        self.limpiar_contenido()
        lbl = tk.Label(self.frame_contenido, text="Gestión de Reservas y Citas", font=self.FONT_TITLE, bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT)
        lbl.pack(anchor="w", padx=30, pady=20)

        tk.Label(self.frame_contenido, text="Aquí podrás gestionar y agendar las citas de tus mascotas.", font=self.FONT_NORMAL, bg=self.COLOR_BG_MAIN, fg="#64748B").pack(anchor="w", padx=30)

    def mostrar_historial(self):
        self.limpiar_contenido()
        lbl = tk.Label(self.frame_contenido, text="Historial Médico y Vacunas", font=self.FONT_TITLE, bg=self.COLOR_BG_MAIN, fg=self.COLOR_TEXT)
        lbl.pack(anchor="w", padx=30, pady=20)

        tk.Label(self.frame_contenido, text="Consulta el carnet de vacunación y notas médicas de tus mascotas.", font=self.FONT_NORMAL, bg=self.COLOR_BG_MAIN, fg="#64748B").pack(anchor="w", padx=30)

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            global usuario_actual
            usuario_actual = None
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VeterinariaApp(root)
    root.mainloop()
