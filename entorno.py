import random
import numpy as np

class EntornoAsistente:
    def __init__(self):
        self.estado = self._estado_inicial()
        self.historial = []

    def _estado_inicial(self):
        # 4 características básicas del día:
        hora = random.uniform(0, 1)                  # Hora normalizada
        tareas = random.randint(0, 5)                # Nº tareas pendientes
        mensajes_sin_leer = random.randint(0, 3)     # Simulación WhatsApp
        necesidad_nota = random.choice([0.0, 1.0])   # 1 si hay algo que guardar
        return np.array([hora, tareas, mensajes_sin_leer, necesidad_nota], dtype=np.float32)

    def obtener_estado(self):
        return self.estado

    def aplicar_accion(self, accion):
        """
        Acciones:
        0 - No hacer nada
        1 - Enviar recordatorio
        2 - Crear tarea
        3 - Guardar nota
        4 - Enviar mensaje WhatsApp
        """
        recompensa = 0

        if accion == 1:
            recompensa = 1 if self.estado[1] > 0 else -1  # solo si hay tareas
        elif accion == 2:
            recompensa = 1 if random.random() > 0.2 else -1  # 80% que sea útil
        elif accion == 3:
            recompensa = 1 if self.estado[3] == 1.0 else -1
        elif accion == 4:
            recompensa = 1 if self.estado[2] > 0 else -1
        else:
            recompensa = 0  # no hacer nada

        self.historial.append((self.estado.tolist(), int(accion), recompensa))
        self.estado = self._estado_inicial()
        return self.estado, recompensa
