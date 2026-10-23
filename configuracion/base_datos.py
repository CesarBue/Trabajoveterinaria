import sqlite3
import os

DB_PATH = os.path.expanduser("~")
DB_NAME = os.path.join(DB_PATH, "veterinaria.db")

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    return conexion

def inicializar_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad REAL,
            peso REAL,
            observaciones TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER,
            servicio TEXT NOT NULL,
            fecha_reserva TEXT NOT NULL,
            costo_estimado REAL,
            estado TEXT,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_medico (
            id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER,
            tipo_registro TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (nombre) VALUES ('Cesar David (Dueño)')")

    conexion.commit()
    conexion.close()
