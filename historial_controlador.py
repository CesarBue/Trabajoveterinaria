from configuracion.base_datos import obtener_conexion

class HistorialControlador:

    @staticmethod
    def registrar_historial(id_mascota, tipo_registro, descripcion, fecha, proxima_dosis=""):
        if not id_mascota or not tipo_registro or not descripcion.strip() or not fecha.strip():
            return False, ["Todos los campos son obligatorios."]

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO historial_medico (id_mascota, tipo_registro, descripcion, fecha, proxima_dosis)
                VALUES (?, ?, ?, ?, ?)
            """, (id_mascota, tipo_registro, descripcion.strip(), fecha.strip(), proxima_dosis.strip()))
            conexion.commit()
            conexion.close()
            return True, "¡Registro guardado en la historia clínica!"
        except Exception as e:
            return False, [f"Error BD: {str(e)}"]

    @staticmethod
    def obtener_historial_por_mascota(id_mascota):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_historial, tipo_registro, descripcion, fecha, proxima_dosis
                FROM historial_medico WHERE id_mascota = ? ORDER BY fecha DESC
            """, (id_mascota,))
            filas = cursor.fetchall()
            conexion.close()
            return [{"id_historial": f[0], "tipo_registro": f[1], "descripcion": f[2], "fecha": f[3], "proxima_dosis": f[4]} for f in filas]
        except Exception:
            return []