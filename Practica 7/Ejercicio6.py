def measure_performance(agent, action, environment, history_places):
    """
    Actualiza el rendimiento del agente en función de la acción y el estado del entorno.

    La función evalúa el rendimiento del agente con base en su eficiencia al limpiar el entorno,
    el tipo de movimiento realizado, y la cantidad de veces que visita lugares. 

    Parámetros:
        agent: El agente aspiradora (con atributos `place` y `performance`).
        action: Acción realizada ('Limpiar', 'Izquierda', 'Derecha', etc.).
        environment: El entorno donde opera el agente (con lugares y cantidades de suciedad).
        history_places: Historial de lugares visitados por el agente para evitar ciclos innecesarios.
    """

    current_place = agent.place  # Lugar actual del agente
    current_amount = current_place.amount  # Cantidad de suciedad en el lugar actual

    # Penalización por realizar acción incorrecta
    if current_amount > 0 and action != "Limpiar":
        agent.performance -= 400  # Penalización por no limpiar cuando debería

    # Recompensa por limpiar correctamente
    if action == "Limpiar":
        if current_amount == max(environment.amounts):
            agent.performance += 150  # Recompensa extra por limpiar el lugar más sucio
        elif current_amount > 0:
            agent.performance += 20  # Recompensa normal por limpiar un lugar sucio
        else:
            agent.performance -= 400  # Penalización si intenta limpiar un lugar limpio

    # Evaluación de movimientos (Izquierda/Derecha/Arriba/Abajo)
    if action in ["Izquierda", "Derecha"]:
        if current_place in history_places:
            # Si el agente ya ha visitado este lugar y no ha recorrido todo el entorno
            if set(history_places) != set(environment.places):
                agent.performance -= 200  # Penalización por no explorar nuevos lugares
        else:
            history_places.add(current_place)  # Agregar al historial de lugares visitados
            agent.performance += 10  # Recompensa pequeña por explorar un nuevo lugar

    # Recompensa por limpiar todo el entorno
    if not environment.dirt_locations:
        agent.performance += 100  # Recompensa final por limpiar todo el entorno

