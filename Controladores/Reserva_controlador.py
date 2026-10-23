from configuracion.base_datos import obtener_conexion
from modelos.reserva import Reserva

class ReservaControlador:
    
    @staticmethod
    def registrar_reserva(id_mascota, servicio, fecha_reserva, costo_estimado):
        """Valida y registra una nueva cita o cupo de guardería para la mascota."""
        if not id_mascota:
            return False, "Debes seleccionar una mascota."
        if not servicio.strip():
            return False, "El servicio es obligatorio."
        if not fecha_reserva.strip():
            return False, "La fecha de la reserva es obligatoria."

        try:
            costo_num = float(costo_estimado)
            if costo_num < 0:
                return False, "El costo no puede ser negativo."
        except ValueError:
            return False, "El costo estimado debe ser un número válido."

        try:
            nueva_reserva = Reserva(
                id_mascota=int(id_mascota),
                servicio=servicio.strip(),
                fecha_reserva=fecha_reserva.strip(),
                costo_estimado=costo_num,
                estado="Pendiente"
            )
            nueva_reserva.guardar()
            return True, f"¡Reserva de {servicio} agendada con éxito!"
        except Exception as e:
            return False, f"Error al guardar la reserva en la base de datos: {e}"

    @staticmethod
    def obtener_reservas_por_usuario(id_usuario):
        """Consulta todas las reservas asociadas a las mascotas de un usuario específico."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT r.*, m.nombre as nombre_mascota 
            FROM reservas r 
            JOIN mascotas m ON r.id_mascota = m.id_mascota 
            WHERE m.id_usuario = ?
        """, (id_usuario,))
        filas = cursor.fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]
