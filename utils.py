from db import obtener_datos

def calcular_estado(producto):
    try:
        df = obtener_datos()
        fila = df[df['nombre'] == producto]

        if fila.empty:
            return "Producto no encontrado"

        fila = fila.iloc[0]
        total, minimo, maximo = fila['cantidad'], fila['min_stock'], fila['max_stock']

        if None in [total, minimo, maximo]:
            return "Datos incompletos"

        if total <= minimo:
            return "Bajo"
        elif total <= maximo:
            return "Alerta"
        else:
            return "OK"

    except Exception as e:
        return f"Error: {str(e)}"

def recalcular_estado_global(producto):
    try:
        df = obtener_datos()
        fila = df[df['nombre'] == producto]

        if fila.empty:
            return "Producto no encontrado"

        fila = fila.iloc[0]
        fisico, minimo, maximo = fila['cantidad'], fila['min_stock'], fila['max_stock']

        if None in [fisico, minimo, maximo]:
            return "Datos incompletos"

        if fisico <= minimo:
            return "Bajo"
        elif fisico <= maximo:
            return "Alerta"
        else:
            return "OK"

    except Exception as e:
        return f"Error: {str(e)}"

