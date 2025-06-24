from db import obtener_datos

def calcular_estado(producto):
    df = obtener_datos()
    fila = df[df['producto'] == producto].iloc[0]
    total, minimo, maximo = fila['Total'], fila['Min'], fila['Max']

    if total <= minimo:
        return "Bajo"
    elif total <= maximo:
        return "Alerta"
    else:
        return "OK"

def recalcular_estado_global(producto):
    df = obtener_datos()
    fila = df[df['producto'] == producto].iloc[0]
    fisico, minimo, maximo = fila['Fisico'], fila['Min'], fila['Max']

    if fisico <= minimo:
        estado = "Bajo"
    elif fisico <= maximo:
        estado = "Alerta"
    else:
        estado = "OK"

    return estado
