from configuracion.base_datos import obtener_conexion

class MascotaControlador:

    @staticmethod
    def registrar_mascota(id_usuario, nombre, tipo, raza, edad, peso, observaciones):
        """Valida e inserta una nueva mascota asociada al usuario en la base de datos."""
        errores = []
        if not nombre.strip():
            errores.append("El nombre de la mascota es obligatorio.")
        if not tipo:
            errores.append("Debe seleccionar un tipo de mascota.")
        if not raza.strip():
            errores.append("La raza es obligatoria.")
        
        try:
            edad = float(edad)
            if edad < 0:
                errores.append("La edad no puede ser negativa.")
        except ValueError:
            errores.append("La edad debe ser un número válido.")

        try:
            peso = float(peso)
            if peso < 0:
                errores.append("El peso no puede ser negativo.")
        except ValueError:
            errores.append("El peso debe ser un número válido.")

        if errores:
            return False, errores

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO mascotas (id_usuario, nombre, tipo, raza, edad, peso, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_usuario, nombre.strip(), tipo, raza.strip(), edad, peso, observaciones.strip()))
            conexion.commit()
            conexion.close()
            return True, "¡Mascota registrada con éxito!"
        except Exception as e:
            return False, [f"Error en la base de datos: {str(e)}"]

    @staticmethod
    def listar_mascotas_usuario(id_usuario):
        """Devuelve la lista de mascotas registradas por el usuario."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_mascota, nombre, tipo, raza, edad, peso, observaciones
                FROM mascotas
                WHERE id_usuario = ?
            """, (id_usuario,))
            filas = cursor.fetchall()
            conexion.close()

            mascotas = []
            for f in filas:
                mascotas.append({
                    "id_mascota": f[0],
                    "nombre": f[1],
                    "tipo": f[2],
                    "raza": f[3],
                    "edad": f[4],
                    "peso": f[5],
                    "observaciones": f[6]
                })
            return mascotas
        except Exception:
            return []
