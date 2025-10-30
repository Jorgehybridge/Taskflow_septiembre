from SRC.database import DBManager, crear_tabla
from SRC.modelos import Tarea
import os

# Ensure DB and tables exist in current folder
crear_tabla()

manager = DBManager()

# Create a new test task
nueva = Tarea(titulo="tarea prueba completar", fecha_limite="2025-10-16", prioridad="Media", proyecto_id=0, descripcion="prueba")
creada = manager.agregar_tarea(nueva)
print(f"Tarea creada id={creada.id}, estado={creada._estado}")

# Now call def_completar
ok = manager.def_completar(creada.id)
print(f"def_completar returned: {ok}")

# Fetch tasks to confirm
tareas = manager.obtener_tareas()
for t in tareas:
    if t.id == creada.id:
        print(f"Tarea id={t.id} estado={t._estado}")
        break
else:
    print("Tarea no encontrada en listado")
