from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/tasks']

def autenticar_tasks():
    creds = None
    if os.path.exists('token_tasks.json'):
        creds = Credentials.from_authorized_user_file('token_tasks.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_tasks.json', 'w') as token:
            token.write(creds.to_json())
    return build('tasks', 'v1', credentials=creds)

def crear_tarea(titulo, descripcion=None, estado="needsAction"):
    service = autenticar_tasks()
    notes = f"status: {estado}"
    if descripcion:
        notes += f"\n{descripcion}"

    body = {
        'title': titulo,
        'notes': notes
    }
    resultado = service.tasks().insert(
        tasklist='@default',
        body=body
    ).execute()
    return resultado.get('id', None)


def eliminar_tarea(task_id):
    service = autenticar_tasks()
    service.tasks().delete(tasklist='@default', task=task_id).execute()

def obtener_tareas():
    service = autenticar_tasks()
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

        # Extraer estado desde notes
        estado = "todo"
        if notes and notes.lower().startswith("status: doing"):
            estado = "doing"
        elif status == "completed":
            estado = "done"

        descripcion = notes.split('\n', 1)[-1] if '\n' in notes else 'Sin descripción'
        tareas[estado].append((title, descripcion, tid))

    return tareas

def actualizar_estado_tarea(task_id, nuevo_estado):
    service = autenticar_tasks()
    tarea = service.tasks().get(tasklist='@default', task=task_id).execute()

    notas = tarea.get('notes', '')
    descripcion = notas.split('\n', 1)[-1] if '\n' in notas else ''

    tarea['notes'] = f"status: {nuevo_estado}\n{descripcion}"

    if nuevo_estado == "done":
        tarea['status'] = "completed"
    else:
        tarea['status'] = "needsAction"

    service.tasks().update(tasklist='@default', task=task_id, body=tarea).execute()
