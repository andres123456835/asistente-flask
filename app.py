from flask import Flask, render_template, request, redirect, url_for
import datetime
from threading import Thread
from gmail_reader import leer_ultimos_correos
from calendar_reader import obtener_eventos_semana
from tasks_manager import obtener_tareas, crear_tarea, eliminar_tarea, actualizar_estado_tarea
from registro_ia import guardar_experiencia, inicializar_base

app = Flask(__name__)
inicializar_base()

# Guardar experiencias en segundo plano
def guardar_en_segundo_plano(estado, accion, recompensa):
    Thread(target=guardar_experiencia, args=(estado, accion, recompensa)).start()

@app.route("/")
def index():
    usuario = request.args.get("usuario", "nina").lower()
    correos = leer_ultimos_correos(3, usuario)
    eventos = obtener_eventos_semana(usuario)
    tareas = obtener_tareas(usuario)
    return render_template("index.html", correos=correos, eventos=eventos, tareas=tareas, usuario=usuario)

@app.route("/nueva-tarea", methods=["POST"])
def nueva_tarea():
    usuario = request.form.get("usuario", "nina").lower()
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    estado = request.form.get("estado", "todo")
    if titulo:
        crear_tarea(titulo, descripcion, estado, usuario)

    estado_actual = {
        "hora": datetime.datetime.now().hour,
        "evento_hoy": len(obtener_eventos_semana(usuario)),
        "num_tareas": sum(len(t) for t in obtener_tareas(usuario).values())
    }
    guardar_en_segundo_plano(estado_actual, "crear", 1)
    return redirect(f"/?usuario={usuario}")

@app.route("/eliminar-tarea/<task_id>")
def eliminar_tarea_web(task_id):
    usuario = request.args.get("usuario", "nina").lower()
    eliminar_tarea(task_id, usuario)

    estado_actual = {
        "hora": datetime.datetime.now().hour,
        "evento_hoy": len(obtener_eventos_semana(usuario)),
        "num_tareas": sum(len(t) for t in obtener_tareas(usuario).values())
    }
    guardar_en_segundo_plano(estado_actual, "eliminar", -1)
    return redirect(f"/?usuario={usuario}")

@app.route("/cambiar-estado/<task_id>/<nuevo_estado>")
def cambiar_estado(task_id, nuevo_estado):
    usuario = request.args.get("usuario", "nina").lower()
    actualizar_estado_tarea(task_id, nuevo_estado, usuario)
    return redirect(url_for("index", usuario=usuario))

@app.route("/mover-tarea/<task_id>/<estado>")
def mover_tarea(task_id, estado):
    usuario = request.args.get("usuario", "nina").lower()
    actualizar_estado_tarea(task_id, estado, usuario)

    recompensa = 0
    if estado == "doing":
        recompensa = 1
    elif estado == "done":
        recompensa = 2

    estado_actual = {
        "hora": datetime.datetime.now().hour,
        "evento_hoy": len(obtener_eventos_semana(usuario)),
        "num_tareas": sum(len(t) for t in obtener_tareas(usuario).values())
    }
    guardar_en_segundo_plano(estado_actual, f"mover_a_{estado}", recompensa)
    return redirect(f"/?usuario={usuario}")

if __name__ == "__main__":
    app.run(debug=True)
