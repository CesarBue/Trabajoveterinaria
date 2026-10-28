from configuracion.base_datos import obtener_conexion
from datetime import datetime

class MascotaControlador:

    @staticmethod
    def registrar_mascota(id_usuario, nombre, tipo, raza, edad_meses, peso, observaciones):
        errores = []
        if not nombre.strip():
            errores.append("El nombre de la mascota es obligatorio.")
        if not tipo:
            errores.append("Debe seleccionar un tipo de mascota.")
        if not raza.strip():
            errores.append("La raza es obligatoria.")

        try:
            edad_meses = int(edad_meses)
            if edad_meses < 0:
                errores.append("La edad en meses no puede ser negativa.")
        except ValueError:
            errores.append("La edad en meses debe ser un número entero válido.")

        try:
            peso = float(peso)
            if peso <= 0:
                errores.append("El peso debe ser mayor a 0 kg.")
        except ValueError:
            errores.append("El peso debe ser un número decimal válido.")

        if errores:
            return False, errores

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO mascotas (id_usuario, nombre, tipo, raza, edad_meses, peso, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_usuario, nombre.strip(), tipo, raza.strip(), edad_meses, peso, observaciones.strip()))
            conexion.commit()
            conexion.close()
            return True, "¡Mascota registrada correctamente!"
        except Exception as e:
            return False, [f"Error BD: {str(e)}"]

    @staticmethod
    def eliminar_mascota(id_mascota):
        """Elimina una mascota y sus registros asociados."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id_mascota = ?", (id_mascota,))
            conexion.commit()
            conexion.close()
            return True, "Mascota eliminada correctamente."
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    @staticmethod
    def listar_mascotas_usuario(id_usuario):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_mascota, nombre, tipo, raza, edad_meses, peso, observaciones
                FROM mascotas WHERE id_usuario = ?
            """, (id_usuario,))
            filas = cursor.fetchall()
            conexion.close()
            return [{"id_mascota": f[0], "nombre": f[1], "tipo": f[2], "raza": f[3], "edad_meses": f[4], "peso": f[5], "observaciones": f[6]} for f in filas]
        except Exception:
            return []

    @staticmethod
    def buscar_mascotas_admin(criterio=""):
        """Permite al administrador buscar por nombre de mascota o nombre del dueño."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
                SELECT m.id_mascota, m.nombre, m.tipo, m.raza, m.edad_meses, m.peso, u.nombre
                FROM mascotas m
                JOIN usuarios u ON m.id_usuario = u.id_usuario
                WHERE m.nombre LIKE ? OR u.nombre LIKE ? OR m.raza LIKE ?
            """
            filtro = f"%{criterio}%"
            cursor.execute(query, (filtro, filtro, filtro))
            filas = cursor.fetchall()
            conexion.close()
            return [{"id_mascota": f[0], "nombre": f[1], "tipo": f[2], "raza": f[3], "edad_meses": f[4], "peso": f[5], "dueno": f[6]} for f in filas]
        except Exception:
            return []

    @staticmethod
    def calcular_semaforo_vacunacion(id_mascota):
        """Calcula el semáforo: 🔴 (Vencida/Sin vacuna), 🟡 (Próxima <= 30 días), 🟢 (Al día)."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT proxima_dosis FROM historial_medico
            WHERE id_mascota = ? AND tipo_registro = 'Vacuna' AND proxima_dosis IS NOT NULL AND proxima_dosis != ''
            ORDER BY proxima_dosis ASC LIMIT 1
        """, (id_mascota,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila or not fila[0]:
            return "🔴", "Sin registro de vacunas o próxima dosis pendiente", "#EF4444"

        try:
            fecha_prox = datetime.strptime(fila[0], "%Y-%m-%d").date()
            hoy = datetime.now().date()
            dias_restantes = (fecha_prox - hoy).days

            if dias_restantes < 0:
                return "🔴", f"Vacuna vencida el {fecha_prox}", "#EF4444"
            elif dias_restantes <= 30:
                return "🟡", f"Próxima vacuna el {fecha_prox} (en {dias_restantes} días)", "#F59E0B"
            else:
                return "🟢", f"Vacunación al día hasta el {fecha_prox}", "#10B981"
        except Exception:
            return "⚪", "Fecha de vacuna no válida", "#6B7280"