from configuracion.base_datos import obtener_conexion

class HistorialMedico:
    def __init__(self, id_mascota, tipo_registro, nombre_detalle, fecha_aplicacion, proxima_dosis=None, lote=None, diagnostico=None, tratamiento=None, id_historial=None):
        self.id_historial = id_historial
        self.id_mascota = id_mascota
        self.tipo_registro = tipo_registro  # 'Vacuna', 'Desparasitacion', 'Consulta'
        self.nombre_detalle = nombre_detalle
        self.fecha_aplicacion = fecha_aplicacion
        self.proxima_dosis = proxima_dosis
        self.lote = lote
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento

    def guardar(self):
        """Guarda un nuevo registro médico o vacuna en la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO historial_medico (id_mascota, tipo_registro, nombre_detalle, fecha_aplicacion, proxima_dosis, lote, diagnostico, tratamiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.id_mascota, self.tipo_registro, self.nombre_detalle, self.fecha_aplicacion, self.proxima_dosis, self.lote, self.diagnostico, self.tratamiento))
        conexion.commit()
        self.id_historial = cursor.lastrowid
        conexion.close()

    @staticmethod
    def obtener_por_mascota(id_mascota):
        """Obtiene todo el historial médico de una mascota específica."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM historial_medico WHERE id_mascota = ?", (id_mascota,))
        filas = cursor.fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]
