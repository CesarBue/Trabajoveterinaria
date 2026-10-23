from configuracion.base_datos import obtener_conexion
from modelos.reserva import Reserva

class ReservaControlador:

    @staticmethod
    def registrar_reserva(id_mascota, servicio, fecha, costo):
        """Valida y registra una nueva cita médica o servicio de guardería."""
        if not id_mascota or not servicio or not fecha or not costo:
            return False, "Todos los campos de la reserva son obligatorios."

        try:
            costo = float(costo)
            if costo < 0:
                return False, "El costo no puede ser negativo."
        except ValueError:
            return False, "El costo debe ser un valor numérico válido."

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO reservas (id_mascota, servicio, fecha_reserva, costo_estimado, estado)
                VALUES (?, ?, ?, ?, 'Confirmada')
            """, (id_mascota, servicio, fecha, costo))
            conexion.commit()
            conexion.close()
            return True, "¡Cita o reserva agendada con éxito!"
        except Exception as e:
            return False, f"Error al guardar la reserva: {str(e)}"

    @staticmethod
    def obtener_reservas_por_usuario(id_usuario):
        """Obtiene el listado completo de reservas vinculadas a las mascotas del usuario."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT r.id_reserva, m.nombre, r.servicio, r.fecha_reserva, r.costo_estimado, r.estado
                FROM reservas r
                JOIN mascotas m ON r.id_mascota = m.id_mascota
                WHERE m.id_usuario = ?
                ORDER BY r.fecha_reserva DESC
            """, (id_usuario,))
            filas = cursor.fetchall()
            conexion.close()

            reservas = []
            for f in filas:
                reservas.append({
                    "id_reserva": f[0],
                    "nombre_mascota": f[1],
                    "servicio": f[2],
                    "fecha_reserva": f[3],
                    "costo_estimado": f[4],
                    "estado": f[5]
                })
            return reservas
        except Exception:
            return []
