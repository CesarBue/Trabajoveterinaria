import sqlite3
import os
import hashlib

local_appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
db_dir = os.path.join(local_appdata, 'veterinaria_app')
os.makedirs(db_dir, exist_ok=True)
DB_NAME = os.path.join(db_dir, "veterinaria.db")

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    return conexion

def encriptar_contrasena(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def inicializar_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL,
            especialidad TEXT,
            telefono TEXT
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

    # Insertar usuario demo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        pass_hash = encriptar_contrasena("123456")
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, contrasena, rol) 
            VALUES ('Cesar David (Dueño)', 'cesar@ejemplo.com', ?, 'Cliente')
        """, (pass_hash,))

    conexion.commit()
    conexion.close()
