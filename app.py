import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# Configuración
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google_credentials"], scope
)
cliente = gspread.authorize(credenciales)

SHEET_ID = "1IIxcoPm9CKesyj86SP1u2wVTzRKrwj3SSha7vYEYRXE"
hoja = cliente.open_by_key(SHEET_ID).sheet1
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# Diccionario visual para estado
estado_visual = {
    "🔴 Bajo": "🔴 Bajo",
    "🟡 Alerta": "🟡 Alerta",
    "🟢 OK": "🟢 OK",
    "Bajo": "🔴 Bajo",
    "Alerta": "🟡 Alerta",
    "OK": "🟢 OK"
}
df_visual = df.copy()
df_visual["Estado"] = df_visual["Estado"].map(estado_visual).fillna("⚪ Sin estado")

# Función para registrar entrada o salida
def actualizar_producto(nombre, cantidad, tipo):
    datos = hoja.get_all_records()
    for idx, fila in enumerate(datos):
        if fila["Material"].strip().lower() == nombre.strip().lower():
            fila_num = idx + 2
            entrada = int(fila["Entrada"])
            salida = int(fila["Salida"])
            if tipo == "entrada":
                entrada += cantidad
                hoja.update_cell(fila_num, 7, entrada)
            elif tipo == "salida":
                salida += cantidad
                hoja.update_cell(fila_num, 8, salida)
            total = entrada - salida
            hoja.update_cell(fila_num, 9, total)
            return True
    return False

# Interfaz con pestañas
tab1, tab2, tab3 = st.tabs(["📦 Inventario", "➕ Registro de producto", "📊 Dashboard"])

# =======================
# TAB 1: Inventario activo
# =======================
with tab1:
    st.title("📦 Inventario Arismendy")
    st.dataframe(df_visual)

    st.subheader("➕ Registrar entrada de producto")
    with st.form("entrada_form"):
        nombre_entrada = st.text_input("Nombre del producto")
        cantidad_entrada = st.number_input("Cantidad a ingresar", min_value=1, step=1)
        enviar = st.form_submit_button("Registrar entrada")
        if enviar:
            ok = actualizar_producto(nombre_entrada, cantidad_entrada, tipo="entrada")
            if ok:
                st.success("✅ Entrada registrada correctamente.")
            else:
                st.error("❌ Producto no encontrado.")

    st.subheader("➖ Registrar salida de producto")
    with st.form("salida_form"):
        nombre_salida = st.text_input("Nombre del producto", key="salida_nombre")
        cantidad_salida = st.number_input("Cantidad a retirar", min_value=1, step=1, key="salida_cantidad")
        retirar = st.form_submit_button("Registrar salida")
        if retirar:
            ok = actualizar_producto(nombre_salida, cantidad_salida, tipo="salida")
            if ok:
                st.success("✅ Salida registrada correctamente.")
            else:
                st.error("❌ Producto no encontrado.")

# ===========================
# TAB 2: Registro de productos
# ===========================
with tab2:
    st.header("🆕 Registrar nuevo producto")
    with st.form("registro_nuevo_producto"):
        codigo = st.text_input("Código")
        material = st.text_input("Nombre del material")
        medida = st.selectbox("Unidad de medida", ["RLL", "UND", "GAL", "MTS", "KG"])
        minimo = st.number_input("Cantidad mínima", min_value=0, step=1)
        maximo = st.number_input("Cantidad máxima", min_value=1, step=1)
        registrar = st.form_submit_button("Registrar producto")
        if registrar:
            if not codigo or not material:
                st.warning("❗ Debes ingresar el código y el nombre del material.")
            elif minimo >= maximo:
                st.warning("❗ El valor mínimo debe ser menor que el máximo.")
            else:
                datos = hoja.get_all_records()
                nueva_fila = [
                    len(datos) + 1,  # Item
                    codigo,
                    material,
                    medida,
                    int(minimo),
                    int(maximo),
                    0,
                    0,
                    0,
                    ""  # Estado lo calcula Sheets
                ]
                hoja.append_row(nueva_fila)
                st.success("✅ Producto registrado exitosamente.")

# ===========================
# TAB 3: Dashboard de análisis
# ===========================
with tab3:
    st.header("📊 Dashboard de Inventario")

    df_dashboard = df.copy()
    df_dashboard["Rotacion"] = df_dashboard["Entrada"] + df_dashboard["Salida"]

    # Métricas clave
    total_productos = len(df_dashboard)
    total_entrada = df_dashboard["Entrada"].sum()
    total_salida = df_dashboard["Salida"].sum()
    promedio_total = df_dashboard["Total"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Productos totales", total_productos)
    col2.metric("Total entradas", total_entrada)
    col3.metric("Total salidas", total_salida)

    st.metric("Promedio de inventario", f"{promedio_total:.2f}")

    # Gráfico de torta por estado
    estado_count = df_dashboard["Estado"].value_counts().reset_index()
    estado_count.columns = ["Estado", "Cantidad"]
    fig_estado = px.pie(
        estado_count,
        values="Cantidad",
        names="Estado",
        title="Distribución de productos por estado",
        color_discrete_sequence=["red", "orange", "green"]
    )
    st.plotly_chart(fig_estado)

    # Top 10 por rotación
    top_rotacion = df_dashboard.sort_values(by="Rotacion", ascending=False).head(10)
    fig_rotacion = px.bar(
        top_rotacion,
        x="Material",
        y="Rotacion",
        title="Top 10 productos con mayor rotación",
        color="Rotacion",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_rotacion)


