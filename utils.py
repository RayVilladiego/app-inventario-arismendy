# utils.py

def calcular_estado(total, minimo, maximo):
    if total < minimo:
        return "Bajo"
    elif total < minimo + 0.2 * (maximo - minimo):
        return "Alerta"
    else:
        return "OK"
