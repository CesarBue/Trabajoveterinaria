from configuracion.base_datos import obtener_conexion

class Mascota:
    def __init__(self, id_usuario, nombre, tipo, raza, edad, peso, observaciones="", id_mascota=None):
        self.id_mascota = id_mascota
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.observaciones = observaciones

    def guardar(self):
        """Guarda o registra una nueva mascota en la base de datos SQLite."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO mascotas (id_usuario, nombre, tipo, raza, edad, peso, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.id_usuario, self.nombre, self.tipo, self.raza, self.edad, self.peso, self.observaciones))
        conexion.commit()
        self.id_mascota = cursor.lastrowid
        conexion.close()

    @staticmethod
    def obtener_por_usuario(id_usuario):
        """Retorna una lista con todas las mascotas asociadas a un usuario específico."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mascotas WHERE id_usuario = ?", (id_usuario,))
        filas = cursor.fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]

    @staticmethod
    def obtener_por_id(id_mascota):
        """Busca y retorna una mascota por su ID único."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mascotas WHERE id_mascota = ?", (id_mascota,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None
