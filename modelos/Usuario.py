from configuracion.base_datos import obtener_conexion

class Usuario:
    def __init__(self, nombre, email, contrasena, rol="Cliente", id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

    def registrar(self):
        """Registra un nuevo usuario en la base de datos SQLite."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contrasena, rol)
                VALUES (?, ?, ?, ?)
            """, (self.nombre, self.email, self.contrasena, self.rol))
            conexion.commit()
            self.id_usuario = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def iniciar_sesion(email, contrasena):
        """Valida las credenciales de un usuario para permitir el acceso al sistema."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM usuarios WHERE email = ? AND contrasena = ?
        """, (email, contrasena))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None
