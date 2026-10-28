from configuracion.base_datos import obtener_conexion, encriptar_contrasena

class Usuario:
    def __init__(self, nombre, email, contrasena, rol="Cliente", especialidad=None, telefono=None, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol
        self.especialidad = especialidad
        self.telefono = telefono

    def registrar(self):
        """Registra un nuevo usuario con la contraseña hasheada."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            pass_hash = encriptar_contrasena(self.contrasena)
            
            # Asegurar que especialidad y teléfono sean nulos si están vacíos
            esp = self.especialidad if self.especialidad and self.especialidad.strip() != "" else None
            tel = self.telefono if self.telefono and self.telefono.strip() != "" else None

            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contrasena, rol, especialidad, telefono)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.nombre, self.email, pass_hash, self.rol, esp, tel))
            conexion.commit()
            self.id_usuario = cursor.lastrowid
            return True, "¡Registro exitoso! Ya puedes iniciar sesión."
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "El correo electrónico ya está registrado."
            return False, f"Error al registrar usuario: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def iniciar_sesion(email, contrasena):
        """Valida credenciales comparando el hash de la contraseña."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        pass_hash = encriptar_contrasena(contrasena)
        cursor.execute("""
            SELECT id_usuario, nombre, email, rol, especialidad, telefono 
            FROM usuarios 
            WHERE email = ? AND contrasena = ?
        """, (email, pass_hash))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return {
                "id_usuario": fila[0],
                "nombre": fila[1],
                "email": fila[2],
                "rol": fila[3],
                "especialidad": fila[4],
                "telefono": fila[5]
            }
        return None
