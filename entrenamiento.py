from entorno import EntornoAsistente
from agente import Agente
import numpy as np

def entrenar_agente(episodios=1000):
    env = EntornoAsistente()
    agente = Agente(estado_dim=4, accion_dim=5)

    for episodio in range(episodios):
        estado = env.obtener_estado()
        accion = agente.elegir_accion(estado)
        estado_siguiente, recompensa = env.aplicar_accion(accion)

        agente.entrenar(estado, accion, recompensa, estado_siguiente)

        if episodio % 50 == 0:
            print(f"[{episodio}] Acción: {accion}, Recompensa: {recompensa}")

    print("Entrenamiento terminado.")