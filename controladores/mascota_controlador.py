from configuracion.base_datos import obtener_conexion

class MascotaControlador:
    
    @staticmethod
    def obtener_mascotas_por_usuario(id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mascotas WHERE id_usuario = ?", (id_usuario,))
        mascotas = cursor.fetchall()
        conexion.close()
        return mascotas

    @staticmethod
    def registrar_mascota(id_usuario, nombre, tipo, raza, edad, peso, observaciones):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO mascotas (id_usuario, nombre, tipo, raza, edad, peso, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_usuario, nombre, tipo, raza, edad, peso, observaciones))
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar_mascota(id_mascota):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM mascotas WHERE id_mascota = ?", (id_mascota,))
        conexion.commit()
        conexion.close()
