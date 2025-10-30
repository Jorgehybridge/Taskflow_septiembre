# Ruta recomendada para git add (desde la raíz del repositorio):
# git add "SRC/database.py"

import sqlite3
from .modelos import Tarea, Proyecto
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



# Module-level helper removed; use DBManager.agregar_tarea instead
class DBManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        if not os.path.exists(self.db_name):
            crear_tabla()
    def agregar_tarea(self, tarea: Tarea) -> Tarea:
        """Insert a Tarea into the tareas table and return it with id set."""
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
    

    

    def actualizar_tarea(self, tarea_id: int) -> bool:
        """Mark the tarea with given id as completed.

        Returns True if a row was updated, False otherwise.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tareas
            SET estado = ?
            WHERE id = ?
        """, ("Completada", tarea_id))
        updated = cursor.rowcount
        conn.commit()
        conn.close()
        return updated > 0
    
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
    
    def obtener_tareas(self, estado: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        sql="SELECT * FROM tareas"
        params=[]    
        if estado:
            sql += " WHERE estado = ?"
            params.append(estado)
        sql += " ORDER BY fecha_limite ASC"
        cursor.execute(sql, params)
        filas = cursor.fetchall()
        tareas = []
        for fila in filas:
            tarea = Tarea(
                id=fila['id'],
                titulo=fila['titulo'],
                descripcion=fila['descripcion'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                estado=fila['estado'],
                proyecto_id=fila['proyecto_id']
            )
            tareas.append(tarea)
        conn.close()
        return tareas
    
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
    
    tarea_creada = manager.crear_tabla(tarea_prueba)
    print(f"Tarea creada y ID asignado: {tarea_creada.id}")