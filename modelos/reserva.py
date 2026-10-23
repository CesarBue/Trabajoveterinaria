from configuracion.base_datos import obtener_conexion

class Reserva:
    def __init__(self, id_mascota, servicio, fecha_reserva, costo_estimado=0.0, estado="Pendiente", id_reserva=None):
        self.id_reserva = id_reserva
        self.id_mascota = id_mascota
        self.servicio = servicio  # 'Consulta', 'Guarderia', 'Peluqueria'
        self.fecha_reserva = fecha_reserva
        self.costo_estimado = costo_estimado
        self.estado = estado

    def guardar(self):
        """Registra una nueva reserva o cita en la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO reservas (id_mascota, servicio, fecha_reserva, estado, costo_estimado)
            VALUES (?, ?, ?, ?, ?)
        """, (self.id_mascota, self.servicio, self.fecha_reserva, self.estado, self.costo_estimado))
        conexion.commit()
        self.id_reserva = cursor.lastrowid
        conexion.close()

    @staticmethod
    def obtener_todas():
        """Retorna todas las reservas registradas (útil para el panel de empleados)."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM reservas")
        filas = cursor.fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]
