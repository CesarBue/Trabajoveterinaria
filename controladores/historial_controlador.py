from configuracion.base_datos import obtener_conexion

class HistorialControlador:

    @staticmethod
    def registrar_historial(id_mascota, tipo_registro, descripcion, fecha):
        """Registra una vacuna, desparasitación o consulta en el historial médico."""
        errores = []
        if not id_mascota:
            errores.append("Debe seleccionar una mascota.")
        if not tipo_registro:
            errores.append("El tipo de registro es obligatorio.")
        if not descripcion.strip():
            errores.append("La descripción no puede estar vacía.")
        if not fecha.strip():
            errores.append("La fecha es obligatoria.")

        if errores:
            return False, errores

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO historial_medico (id_mascota, tipo_registro, descripcion, fecha)
                VALUES (?, ?, ?, ?)
            """, (id_mascota, tipo_registro, descripcion, fecha))
            conexion.commit()
            conexion.close()
            return True, "¡Historial médico registrado con éxito!"
        except Exception as e:
            return False, [f"Error en la base de datos: {str(e)}"]

    @staticmethod
    def obtener_historial_por_mascota(id_mascota):
        """Obtiene todo el historial médico y de vacunación de una mascota específica."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                id_historial, tipo_registro, descripcion, fecha
                FROM historial_medico
                WHERE id_mascota = ?
                ORDER BY fecha DESC
            """, (id_mascota,))
            filas = cursor.fetchall()
            conexion.close()

            historial = []
            for f in filas:
                historial.append({
                    "id_historial": f[0],
                    "tipo_registro": f[1],
                    "descripcion": f[2],
                    "fecha": f[3]
                })
            return historial
        except Exception:
            return []
