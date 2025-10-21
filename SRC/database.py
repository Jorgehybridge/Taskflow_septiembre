# Ruta recomendada para git add (desde la raíz del repositorio):
# git add "SRC/database.py"

import sqlite3
from modelos import Tarea, Proyecto
import os

DATABASE_NAME = 'tareas.db'
def get_connection():
    conn= sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            estado TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
        )
    """)
    try: 
        cursor.execute ("INSERT INTO proyectos(ID, nombre, descripcion, fecha_inicio, estado) VALUES (0, 'tareas', 'tareas sin proyecto', date('now'), 'Activo')")
    except sqlite3.IntegrityError: 
        pass
    conn.commit()
    conn.close()



def crear_tarea(self, tarea: Tarea) -> Tarea:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id))
    
    tarea.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return tarea
class DBManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        if not os.path.exists(self.db_name):
            crear_tabla()
    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id))
        
        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea
    def  obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()
        proyectos = []
        for fila in filas:
            proyecto = Proyecto(
                id=fila['id'],
                nombre=fila['nombre'],
                descripcion=fila['descripcion'],
                fecha_inicio=fila['fecha_inicio'],
                estado=fila['estado']
            )
            proyectos.append(proyecto)
        conn.close()
        return proyectos
if __name__ == '__main__':
    # Bloque de prueba para la clase
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Base de datos {DATABASE_NAME} eliminada.")

    crear_tabla()
    print(f"Base de datos {DATABASE_NAME} y tablas inicializadas correctamente.")
    
    # Prueba del CRUD (CREATE)
    manager = DBManager()
    tarea_prueba = Tarea(
        titulo="Completar Ejercicio de CRUD", 
        fecha_limite="2025-10-30", 
        prioridad="Alta", 
        proyecto_id=0,
        descripcion="Implementar el módulo database.py"
    )
    
    tarea_creada = manager.crear_tarea(tarea_prueba)
    print(f"Tarea creada y ID asignado: {tarea_creada.id}")