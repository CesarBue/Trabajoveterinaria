import sqlite3
import os

local_appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
db_dir = os.path.join(local_appdata, 'veterinaria_app')
os.makedirs(db_dir, exist_ok=True)
DB_NAME = os.path.join(db_dir, "veterinaria.db")

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def inicializar_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Tabla Usuarios con todos los roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL -- 'Cliente', 'Admin', 'Veterinario', 'Cuidador', 'Estilista'
        )
    """)

    # 2. Tabla Mascotas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad_meses INTEGER NOT NULL,
            peso REAL NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE
        )
    """)

    # 3. Tabla Reservas con soporte para Guardería (Fecha fin y notas de alimentación)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER NOT NULL,
            servicio TEXT NOT NULL,
            rol_encargado TEXT NOT NULL,
            fecha_reserva TEXT NOT NULL,
            fecha_fin TEXT,
            observaciones_servicio TEXT,
            costo_estimado REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota) ON DELETE CASCADE
        )
    """)

    # Migración suave en caso de que la tabla ya existiera
    cursor.execute("PRAGMA table_info(reservas)")
    columnas = [col[1] for col in cursor.fetchall()]
    if "fecha_fin" not in columnas:
        cursor.execute("ALTER TABLE reservas ADD COLUMN fecha_fin TEXT")
    if "observaciones_servicio" not in columnas:
        cursor.execute("ALTER TABLE reservas ADD COLUMN observaciones_servicio TEXT")

    # 4. Historial Médico
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_medico (
            id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER NOT NULL,
            tipo_registro TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha TEXT NOT NULL,
            proxima_dosis TEXT,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota) ON DELETE CASCADE
        )
    """)

    # Seed data inicial
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO usuarios (nombre, username, password, rol) VALUES (?, ?, ?, ?)
        """, [
            ("Administrador General", "admin", "admin123", "Admin"),
            ("César David (Dueño)", "cesar", "1234", "Cliente"),
            ("Dr. Roberto Gómez", "vet_roberto", "1234", "Veterinario"),
            ("María Estilista", "est_maria", "1234", "Estilista"),
            ("Carlos Cuidador", "cuid_carlos", "1234", "Cuidador")
        ])

    conexion.commit()
    conexion.close()