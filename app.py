from flask import Flask, render_template, request, redirect, url_for, render_template_string, Response
from SRC.database import DBManager, crear_tabla
from SRC.modelos import Tarea, Proyecto

app = Flask(__name__)
db_manager = DBManager()

@app.route('/')
def index():
    tareas_pendientes = db_manager.obtener_tareas(estado="Pendiente")
    proyectos = db_manager.obtener_proyectos()
    return render_template('index.html', tareas=tareas_pendientes, proyectos=proyectos)

@app.route('/agregar_tarea', methods=['GET', 'POST'])
def agregar_tarea():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        limite = request.form.get('fecha_limite')
        prioridad = request.form.get('prioridad')

        proyecto_id = request.form.get('proyecto_id')
        nueva_tarea = Tarea(titulo=titulo, 
                            descripcion=descripcion, 
                            fecha_limite=limite, prioridad=prioridad, 
                            proyecto_id=proyecto_id, estado="Pendiente")
        db_manager.agregar_tarea(nueva_tarea)
        return redirect(url_for('index'))
    return render_template('agregar_tarea.html', proyectos=db_manager.obtener_proyectos())


@app.route('/completar/<int:tarea_id>', methods=['POST'])

def completar_tarea(tarea_id):
    """Mark a tarea as completed and redirect to index."""
    db_manager.actualizar_tarea(tarea_id)
    return redirect(url_for('index'))
if __name__ == '__main__':
    # crea las tablas al arrancar (usar la función del módulo)
    crear_tabla()
    #print("Base de datos y tablas creadas correctamente.")
    app.run(debug=True)