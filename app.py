import streamlit as st
import pandas as pd
from calculos import realizar_calculos, cargar_datos_muestra
from pdf_reporte import generar_pdf
from textos import teoria

st.set_page_config(page_title="Calibración EPA Método 5", layout="wide")

# ==========================================
# HERRAMIENTAS NECESARIAS
# ==========================================
if 'unit_system' not in st.session_state:
    st.session_state.unit_system = 'metrico'
    st.session_state.is_sample_data = False

if 'num_corridas' not in st.session_state:
    st.session_state.num_corridas = 5

def marcar_dato_manual():
    """Si el usuario tipea un número, bajamos la bandera de datos de muestra"""
    st.session_state.is_sample_data = False

columnas_base = [
    'theta', 'delta_h', 'vol_inicial', 'vol_final', 
    't_salida_inicial', 't_salida_final', 'k_prime', 't_amb',
    'V_m', 'V_m_std', 'V_cr_std', 'Y', 'delta_h_at'
]

def toggle_units():
    # Cambiar el sistema
    st.session_state.unit_system = 'imperial' if st.session_state.unit_system == 'metrico' else 'metrico'
    
    # Si los datos actuales eran de muestra, los reseteamos a cero al cambiar unidad
    if st.session_state.is_sample_data:
        st.session_state.p_bar = 0.0
        st.session_state.df_corridas = pd.DataFrame([[0.0]*13 for _ in range(st.session_state.num_corridas)], columns=columnas_base)
        st.session_state.is_sample_data = False # Apagamos la bandera tras borrar
        if 'editor_corridas' in st.session_state:
            del st.session_state['editor_corridas']

@st.dialog("Confirmar reemplazo")
def confirmar_carga_muestra():
    st.warning("Ya tenés datos cargados manualmente en la tabla, ¿querés borrarlos y cargar los datos de muestra?")
    c1, c2 = st.columns(2)
    if c1.button("Sí, cargar muestra", use_container_width=True):
        cargar_datos_muestra(columnas_base)
        st.session_state.num_corridas = 8
        st.rerun()  # Recarga la app aplicando los cambios
    if c2.button("Cancelar", use_container_width=True):
        st.rerun()  # Cierra la ventana sin hacer nada

# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================
col_titulo, col_unidades, col_muestra, col_teoria = st.columns([3, 1, 1, 1])

with col_titulo:
    st.title("Calibración de Consola - Método 5")

with col_unidades:
    st.write("")
    # Botón para cambiar unidades
    if st.session_state.unit_system == 'metrico':
        st.button("Cambiar al Sistema Imperial", on_click=toggle_units, use_container_width=True)
    else:
        st.button("Cambiar al Sistema Internacional", on_click=toggle_units, use_container_width=True)

with col_muestra:
    st.write("")
    if st.button("Cargar datos de muestra", use_container_width=True):
        # Verifica si hay datos manuales (distintos de cero)
        hay_datos_manuales = False
        hay_datos_manuales = (
            'df_corridas' in st.session_state
            and not st.session_state.is_sample_data
            and (st.session_state.df_corridas >0).any().any()
        )
        if hay_datos_manuales:
            confirmar_carga_muestra() # Abre el Pop-out
        else:
            cargar_datos_muestra(columnas_base) # Carga directo
            st.rerun()

with col_teoria:
    st.write("") # Espacio para alinear el botón
    # Este botón llama a la función de la ventana emergente
    if st.button("Ver teoría", use_container_width=True):
        teoria()

# Cargamos los datos
col_subt, col_advertencia, _ = st.columns([8, 9, 15])

with col_subt:
    st.markdown("")
    st.markdown("### Condiciones iniciales")

with col_advertencia:
    # Advertencia si está en sistema imperial y definiciones
    if st.session_state.unit_system == 'imperial':
        st.error("ADVERTENCIA: está configurado el Sistema Imperial de unidades.")
        u_vol, u_temp, u_pres, u_h2o = "ft³", "°F", "in. Hg", "in. H₂O"
    else:
        u_vol, u_temp, u_pres, u_h2o = "m³", "°C", "mm Hg", "mm H₂O"

col_amb1, col_amb2, col_amb3, col_amb4 = st.columns(4)
with col_amb1:
    temp_amb = st.number_input(f"Temperatura Ambiente [{u_temp}]", value=19.0, format="%.2f", step=0.1)
with col_amb2:
    humedad = st.number_input("Humedad [%]", value=50.0, format="%.1f", step=1.0)
with col_amb3:
    p_bar = st.number_input(f"Presión Barométrica ($P_{{bar}}$) [{u_pres}]", format="%.2f", step=1.0, key="p_bar", on_change=marcar_dato_manual)
with col_amb4:
    num_corridas = st.number_input("Cantidad de corridas (la normativa exige un mínimo de tres):", min_value=3, value=5, key="num_corridas", step=1)

st.markdown(
    """
    <div style="display: flex; align-items: baseline; gap: 15px; margin-bottom: 10px;">
        <h3 style="margin: 0;">Datos de las corridas</h3>
        <span style="font-size: 16px; color: gray;">Podés editar las primeras ocho columnas.</span>
    </div>
    """, 
    unsafe_allow_html=True
)
# Creamos la tabla
if 'df_corridas' not in st.session_state:
    st.session_state.df_corridas = pd.DataFrame([[0.0]*13 for _ in range(num_corridas)], columns=columnas_base)

# Redimensionamiento dinámico
filas_actuales = len(st.session_state.df_corridas)
if num_corridas > filas_actuales:
    # Si incrementaste el número, añade filas vacías al final conservando las de arriba
    filas_nuevas = pd.DataFrame([[0.0]*13 for _ in range(num_corridas - filas_actuales)], columns=columnas_base)
    st.session_state.df_corridas = pd.concat([st.session_state.df_corridas, filas_nuevas], ignore_index=True)
elif num_corridas < filas_actuales:
    # Si disminuiste el número, recorta desde el final manteniendo los datos superiores
    st.session_state.df_corridas = st.session_state.df_corridas.iloc[:num_corridas]

# Forzamos el índice visual de la tabla
st.session_state.df_corridas.index = range(1, num_corridas + 1)

# Configuramos la visualización de la tabla para que tenga las unidades y formato correcto
config_columnas = {
    "theta": st.column_config.NumberColumn("Tiempo  [min]", format="%.2f"),
    "delta_H": st.column_config.NumberColumn(f"ΔH  [{u_h2o}]", format="%.2f"),
    #"Vw": st.column_config.NumberColumn(f"Vw: volumen patrón húmedo [{u_vol}]", format="%.4f"),
    #"Vm": st.column_config.NumberColumn(f"Vm: volumen medidor [{u_vol}]", format="%.4f"),
    "vol_inicial": st.column_config.NumberColumn(f"Volumen inicial [{u_vol}]", format="%.3f"),
    "vol_final": st.column_config.NumberColumn(f"Volumen final [{u_vol}]", format="%.3f"),
    #"Tw": st.column_config.NumberColumn(f"Tw: temperatura patrón húmedo [{u_temp}]", format="%.2f"),
    "t_salida_inicial": st.column_config.NumberColumn(f"Temperatura inicial [{u_temp}]", format="%.1f"),
    "t_salida_final": st.column_config.NumberColumn(f"Temperatura final [{u_temp}]", format="%.1f"),
    "k_prime": st.column_config.NumberColumn(f"Coeficiente del orificio [K']", format="%.4f"),
    "t_amb": st.column_config.NumberColumn(f"Temperatura ambiente [{u_temp}]", format="%.1f"),
    "V_m": st.column_config.NumberColumn(f"Vm [{u_vol}]", format="%.4f"),
    "V_m_std": st.column_config.NumberColumn(f"Vm(sdt) [{u_vol}]", format="%.4f"),
    "V_cr_std": st.column_config.NumberColumn(f"Vcr(sdt) [{u_vol}]", format="%.4f"),
    "Y": st.column_config.NumberColumn(f"Y", format="%.4f"),
    "delta_h_at": st.column_config.NumberColumn(f"ΔH@ {u_h2o}]", format="%.4f")
    
}

# st.data_editor es la tabla interactiva de Streamlit
tabla_excel = st.data_editor(
    st.session_state.df_corridas,
    column_config=config_columnas,
    num_rows="fixed",
    disabled=['V_m', 'V_m_std', 'V_cr_std', 'Y', 'delta_h_at'],
    use_container_width=True,
    hide_index=False,
    key="editor_corridas",
    on_change=marcar_dato_manual
)

# ==========================================
# PROCESAMIENTO Y RESULTADOS
# ==========================================
st.session_state.df_corridas = tabla_excel
tm_avg, y_factor, delta_h_at = realizar_calculos(
    st.session_state.df_corridas, p_bar, st.session_state.unit_system
)

st.markdown("---")
col_final, col_res1, col_res2, _ = st.columns([1, 1, 1, 3])
col_final.markdown("### Resultados")
col_res1.metric("Factor de Calibración ($Y$)", f"{y_factor:.4f}")
col_res2.metric("Delta H@ ($\Delta H_@$)", f"{delta_h_at:.4f} {u_h2o}")

#Exportación 
#st.markdown("---")
#pdf_bytes = generar_pdf(tabla_excel, p_bar, tm_avg, y_factor, delta_h_at, st.session_state.unit_system)

#st.download_button(
#    label="📄 Imprimir un PDF con toda la información",
#    data=pdf_bytes,
#    file_name="Reporte_Calibracion_Metodo5.pdf",
#    mime="application/pdf"
#)