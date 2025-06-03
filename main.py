from tasks_manager import crear_tarea, obtener_tareas

if __name__ == "__main__":
    print("Creando tarea...")
    crear_tarea("Revisar correos importantes")

    print("\nTareas actuales:")
    tareas = obtener_tareas()
    for i, (titulo, estado) in enumerate(tareas, 1):
        print(f"{i}. {titulo} - Estado: {estado}")
