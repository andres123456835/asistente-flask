from gmail_reader import leer_ultimos_correos
from calendar_reader import obtener_eventos_hoy
from tasks_manager import crear_tarea, obtener_tareas

def asistente_diario():
    print("========== ASISTENTE PERSONAL ==========\n")

    # 1. Correos recientes
    correos = leer_ultimos_correos(3)
    print("📩 Correos recientes:")
    for i, (de, asunto) in enumerate(correos, 1):
        print(f"{i}. De: {de} | Asunto: {asunto}")

        # Crear tarea si el asunto contiene la palabra clave
        if any(palabra in asunto.lower() for palabra in ["tarea", "urgente", "pendiente"]):
            crear_tarea(f"Responder: {asunto}")

    print("\n📅 Eventos de hoy:")
    eventos = obtener_eventos_hoy()
    for i, (hora, titulo) in enumerate(eventos, 1):
        print(f"{i}. {titulo} a las {hora}")

    print("\n✅ Tareas actuales:")
    tareas = obtener_tareas()
    for i, (titulo, estado) in enumerate(tareas, 1):
        print(f"{i}. {titulo} [{estado}]")

    print("\n🔁 Proceso completado.\n")

if __name__ == "__main__":
    asistente_diario()
