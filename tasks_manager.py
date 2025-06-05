from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json

SCOPES = ['https://www.googleapis.com/auth/tasks']

def autenticar_tasks(usuario="nina"):
    creds = None
    token_file = f"token_tasks_{usuario}.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        creds_env_var = f"GOOGLE_CREDS_TASKS_{usuario.upper()}"
        creds_data = json.loads(os.environ[creds_env_var])
        flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('tasks', 'v1', credentials=creds)


def crear_tarea(titulo, descripcion=None, estado="needsAction", usuario="nina"):
    service = autenticar_tasks(usuario)
    notes = f"status: {estado}"
    if descripcion:
        notes += f"\n{descripcion}"

    body = {
        'title': titulo,
        'notes': notes
    }
    resultado = service.tasks().insert(tasklist='@default', body=body).execute()
    return resultado.get('id', None)


def eliminar_tarea(task_id, usuario="nina"):
    service = autenticar_tasks(usuario)
    service.tasks().delete(tasklist='@default', task=task_id).execute()


def obtener_tareas(usuario="nina"):
    service = autenticar_tasks(usuario)
    resultado = service.tasks().list(tasklist='@default').execute()

    tareas = {
        "todo": [],
        "doing": [],
        "done": []
    }

    for t in resultado.get('items', []):
        title = t.get('title', '')
        notes = t.get('notes', '')
        status = t.get('status', 'needsAction')
        tid = t.get('id')

        # Detectar estado y descripción según el formato
        if notes and notes.lower().startswith("status: doing"):
            estado = "doing"
            descripcion = notes.split('\n', 1)[-1] if '\n' in notes else ''
        elif notes and notes.lower().startswith("status: todo"):
            estado = "todo"
            descripcion = notes.split('\n', 1)[-1] if '\n' in notes else ''
        elif status == "completed":
            estado = "done"
            descripcion = notes if notes else 'Sin descripción'
        else:
            estado = "todo"
            descripcion = notes if notes else 'Sin descripción'

        tareas[estado].append((title, descripcion, tid))

    return tareas


def actualizar_estado_tarea(task_id, nuevo_estado, usuario="nina"):
    service = autenticar_tasks(usuario)
    tarea = service.tasks().get(tasklist='@default', task=task_id).execute()

    notas = tarea.get('notes', '')
    descripcion = notas.split('\n', 1)[-1] if '\n' in notas else ''

    tarea['notes'] = f"status: {nuevo_estado}\n{descripcion}"
    tarea['status'] = "completed" if nuevo_estado == "done" else "needsAction"

    service.tasks().update(tasklist='@default', task=task_id, body=tarea).execute()
