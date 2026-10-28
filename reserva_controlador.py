from configuracion.base_datos import obtener_conexion
from datetime import datetime

class ReservaControlador:

    MAPA_ROLES = {
        "Consulta Médica 🩺": "Veterinario",
        "Vacunación 💉": "Veterinario",
        "Peluquería / Baño ✂️": "Estilista",
        "Guardería 🏡": "Cuidador"
    }

    @staticmethod
    def validar_fecha_minima(fecha_str):
        try:
            partes = fecha_str.split(" ")[0]
            fecha_res = datetime.strptime(partes, "%Y-%m-%d").date()
            hoy = datetime.now().date()
            if fecha_res <= hoy:
                return False, "La cita debe agendarse con al menos 1 día de anticipación (a partir de mañana)."
            return True, ""
        except ValueError:
            return False, "Formato de fecha inválido. Usa YYYY-MM-DD o YYYY-MM-DD HH:MM."

    @staticmethod
    def calcular_costo_automatico(servicio, peso_kg, raza=""):
        precios_base = {
            "Consulta Médica 🩺": 50000.0,
            "Vacunación 💉": 35000.0,
            "Peluquería / Baño ✂️": 30000.0,
            "Guardería 🏡": 40000.0
        }
        costo = precios_base.get(servicio, 30000.0)

        if peso_kg > 10:
            costo += (peso_kg - 10) * 2000.0

        raza_upper = raza.upper()
        razas_grandes = ["PASTOR", "GOLDEN", "LABRADOR", "HUSKY", "BERNARDO", "DANÉS", "CHOW", "AKITA", "SAMOYEDO", "PUDLE GIGANTE"]
        if any(r in raza_upper for r in razas_grandes):
            costo += 15000.0

        return round(costo, 2)

    @staticmethod
    def registrar_reserva(id_mascota, servicio, fecha_reserva, costo_estimado, fecha_fin="", observaciones_servicio=""):
        valida, msg = ReservaControlador.validar_fecha_minima(fecha_reserva)
        if not valida:
            return False, msg

        if servicio == "Guardería 🏡":
            if not fecha_fin:
                return False, "Para el servicio de guardería debes ingresar la fecha de fin del cuidado."
            valida_fin, msg_fin = ReservaControlador.validar_fecha_minima(fecha_fin)
            if not valida_fin:
                return False, f"Fecha fin inválida: {msg_fin}"

        rol_encargado = ReservaControlador.MAPA_ROLES.get(servicio, "Veterinario")

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM reservas 
            WHERE servicio = ? AND fecha_reserva = ? AND estado != 'Cancelada'
        """, (servicio, fecha_reserva))

        if cursor.fetchone()[0] > 0:
            conexion.close()
            return False, "⚠️ Ya existe una cita agendada para ese servicio en esa misma fecha y hora."

        try:
            cursor.execute("""
                INSERT INTO reservas (id_mascota, servicio, rol_encargado, fecha_reserva, fecha_fin, observaciones_servicio, costo_estimado, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Confirmada')
            """, (id_mascota, servicio, rol_encargado, fecha_reserva, fecha_fin, observaciones_servicio, costo_estimado))
            conexion.commit()
            conexion.close()
            return True, "¡Cita/Reserva agendada exitosamente!"
        except Exception as e:
            conexion.close()
            return False, f"Error BD: {str(e)}"

    @staticmethod
    def completar_reserva(id_reserva):
        """Marca una cita como 'Realizada' para indicar que fue completada y cobrarla."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("UPDATE reservas SET estado = 'Realizada' WHERE id_reserva = ?", (id_reserva,))
            conexion.commit()
            conexion.close()
            return True, "La cita ha sido marcada como REALIZADA."
        except Exception as e:
            return False, f"Error al actualizar estado: {str(e)}"

    @staticmethod
    def obtener_cierre_diario(fecha_dia):
        """Filtra solo las citas realizadas de un día específico y suma las ganancias producidas."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            filtro = f"{fecha_dia}%"
            cursor.execute("""
                SELECT r.id_reserva, m.nombre, u.nombre, r.servicio, r.fecha_reserva, r.costo_estimado, r.rol_encargado
                FROM reservas r
                JOIN mascotas m ON r.id_mascota = m.id_mascota
                JOIN usuarios u ON m.id_usuario = u.id_usuario
                WHERE r.estado = 'Realizada' AND r.fecha_reserva LIKE ?
                ORDER BY r.fecha_reserva ASC
            """, (filtro,))
            filas = cursor.fetchall()
            conexion.close()

            citas = []
            total_dinero = 0.0
            for f in filas:
                costo = float(f[5])
                total_dinero += costo
                citas.append({
                    "id_reserva": f[0],
                    "nombre_mascota": f[1],
                    "dueno": f[2],
                    "servicio": f[3],
                    "fecha_reserva": f[4],
                    "costo_estimado": costo,
                    "rol_encargado": f[6]
                })
            return citas, round(total_dinero, 2)
        except Exception:
            return [], 0.0

    @staticmethod
    def obtener_reservas_por_usuario(id_usuario):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT r.id_reserva, m.nombre, r.servicio, r.fecha_reserva, r.costo_estimado, r.estado, r.rol_encargado, m.id_mascota, r.fecha_fin, r.observaciones_servicio
                FROM reservas r
                JOIN mascotas m ON r.id_mascota = m.id_mascota
                WHERE m.id_usuario = ?
                ORDER BY r.fecha_reserva DESC
            """, (id_usuario,))
            filas = cursor.fetchall()
            conexion.close()
            return [{"id_reserva": f[0], "nombre_mascota": f[1], "servicio": f[2], "fecha_reserva": f[3], "costo_estimado": f[4], "estado": f[5], "rol_encargado": f[6], "id_mascota": f[7], "fecha_fin": f[8], "observaciones_servicio": f[9]} for f in filas]
        except Exception:
            return []

    @staticmethod
    def obtener_reservas_por_rol(rol):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            if rol == "Admin":
                cursor.execute("""
                    SELECT r.id_reserva, m.nombre, u.nombre, r.servicio, r.fecha_reserva, r.costo_estimado, r.estado, r.rol_encargado, m.id_mascota, r.fecha_fin, r.observaciones_servicio
                    FROM reservas r
                    JOIN mascotas m ON r.id_mascota = m.id_mascota
                    JOIN usuarios u ON m.id_usuario = u.id_usuario
                    ORDER BY r.fecha_reserva ASC
                """)
            else:
                cursor.execute("""
                    SELECT r.id_reserva, m.nombre, u.nombre, r.servicio, r.fecha_reserva, r.costo_estimado, r.estado, r.rol_encargado, m.id_mascota, r.fecha_fin, r.observaciones_servicio
                    FROM reservas r
                    JOIN mascotas m ON r.id_mascota = m.id_mascota
                    JOIN usuarios u ON m.id_usuario = u.id_usuario
                    WHERE r.rol_encargado = ?
                    ORDER BY r.fecha_reserva ASC
                """, (rol,))
            filas = cursor.fetchall()
            conexion.close()
            return [{"id_reserva": f[0], "nombre_mascota": f[1], "dueno": f[2], "servicio": f[3], "fecha_reserva": f[4], "costo_estimado": f[5], "estado": f[6], "rol_encargado": f[7], "id_mascota": f[8], "fecha_fin": f[9], "observaciones_servicio": f[10]} for f in filas]
        except Exception:
            return []

    @staticmethod
    def eliminar_reserva(id_reserva):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
            conexion.commit()
            conexion.close()
            return True, "Cita/Reserva eliminada con éxito."
        except Exception as e:
            return False, f"Error: {str(e)}"