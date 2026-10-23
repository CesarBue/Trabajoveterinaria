import sqlite3
import os

DB_NAME = "veterinaria.db"

def obtener_conexion():
    """Establece y retorna una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conexion

def inicializar_base_datos():
    """Crea las tablas necesarias si no existen en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de Usuarios / Roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT DEFAULT 'Cliente'
        )
    """)

    # Tabla de Mascotas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad INTEGER,
            peso REAL,
            observaciones TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
        )
    """)

    # Tabla de Historial Médico y Vacunas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_medico (
            id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER,
            tipo_registro TEXT NOT NULL, -- 'Vacuna', 'Desparasitacion', 'Consulta'
            nombre_detalle TEXT NOT NULL,
            fecha_aplicacion TEXT NOT NULL,
            proxima_dosis TEXT,
            lote TEXT,
            diagnostico TEXT,
            tratamiento TEXT,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota)
        )
    """)

    # Tabla de Reservas y Citas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER,
            servicio TEXT NOT NULL, -- 'Consulta', 'Guarderia', 'Peluqueria'
            fecha_reserva TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente', -- 'Pendiente', 'Completada', 'Cancelada'
            costo_estimado REAL,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota)
        )
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    inicializar_base_datos()
