# calculos.py
import streamlit as st
import pandas as pd
import numpy as np

def realizar_calculos(df, p_bar, unit_system):
    """Realiza los cálculos matemáticos procesando la tabla (DataFrame) completa con las nuevas columnas."""
    
    if unit_system == 'metrico':
        temp_add = 273.15
        k1 = 0.3858
        k4 = 0.0011695
        k_prime_conv = 0.0008309
    else:
        temp_add = 460.0
        k1 = 17.647
        k4 = 0.0319
        k_prime_conv = 1.0

    total_tm_avg, total_y_factor, total_delta_h_at = 0.0, 0.0, 0.0
    corridas_validas = 0

    # Iteramos fila por fila manteniendo tu estructura de bucle original
    for index, row in df.iterrows():
        theta = row['theta']
        delta_h = row['delta_h']
        vol_inicial = row['vol_inicial']
        vol_final = row['vol_final']
        t_salida_inicial = row['t_salida_inicial']
        t_salida_final = row['t_salida_final']
        k_prime = row['k_prime']
        t_amb = row['t_amb']

        # Evitamos divisiones por cero o filas vacías (control de celdas inicializadas en 0)
        if theta <= 0 or vol_final <= vol_inicial or k_prime <= 0:
            continue

        # 1. Volumen neto medido (V_m)
        v_m = vol_final - vol_inicial
        
        # 2. Temperaturas promedio de salida y absolutas
        tm_avg_i = (t_salida_inicial + t_salida_final) / 2
        t_m_abs = tm_avg_i + temp_add
        t_amb_abs = t_amb + temp_add

        # 3. Volúmenes estándar (V_m_std y V_cr_std para el orificio crítico)
        v_m_std = (k1 * v_m * (p_bar + (delta_h / 13.6))) / t_m_abs
        v_cr_std = (k_prime * k_prime_conv * p_bar * theta) / np.sqrt(t_amb_abs)
        
        # 4. Factor Y y Delta H@ de la corrida individual
        y_factor_i = v_cr_std / v_m_std
        delta_h_at_i = (k4 * delta_h * t_m_abs / (p_bar * (y_factor_i ** 2))) * ((theta / v_m) ** 2)

        # Guardamos los resultados calculados de vuelta en las celdas del DataFrame original
        df.at[index, 'V_m'] = round(v_m, 3)
        df.at[index, 'V_m_std'] = round(v_m_std, 3)
        df.at[index, 'V_cr_std'] = round(v_cr_std, 3)
        df.at[index, 'Y'] = round(y_factor_i, 4)
        df.at[index, 'delta_h_at'] = round(delta_h_at_i, 3)

        # Acumulamos los valores para calcular los promedios globales
        total_tm_avg += tm_avg_i
        total_y_factor += y_factor_i
        total_delta_h_at += delta_h_at_i
        corridas_validas += 1

    if corridas_validas > 0:
        return (
            total_tm_avg / corridas_validas,
            total_y_factor / corridas_validas,
            total_delta_h_at / corridas_validas
        )
    else:
        return 0.0, 0.0, 0.0

def cargar_datos_muestra(columnas):
    # Avisamos que se usó el botón automático
    st.session_state.is_sample_data = True  
    st.session_state.num_corridas = 8

    if st.session_state.unit_system == 'metrico':
        st.session_state.p_bar = 769.62
        datos_muestra = [
            [15.0, 7.62, 8.037, 8.172, 20.5, 20.0, 0.2453, 21.1, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 7.62, 8.172, 8.306, 20.0, 20.5, 0.2453, 21.6, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 16.76, 8.306, 8.500, 21.1, 21.1, 0.3508, 21.6, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 16.76, 8.500, 8.694, 21.1, 21.1, 0.3508, 22.2, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 27.94, 8.694, 8.939, 21.1, 21.6, 0.4446, 22.2, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 27.94, 8.939, 9.184, 21.6, 21.6, 0.4446, 22.7, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 50.80, 9.184, 9.513, 21.6, 22.2, 0.6051, 22.7, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 50.80, 9.513, 9.842, 22.2, 22.2, 0.6051, 22.7, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
    else:
        st.session_state.p_bar = 30.30
        datos_muestra = [
            [15.0, 0.30, 283.825, 288.581, 69.0, 68.0, 0.2453, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 0.30, 288.581, 293.330, 68.0, 69.0, 0.2453, 71.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 0.66, 293.330, 300.168, 70.0, 70.0, 0.3508, 71.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 0.66, 300.168, 307.025, 70.0, 70.0, 0.3508, 72.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 1.10, 307.025, 315.679, 70.0, 71.0, 0.4446, 72.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 1.10, 315.679, 324.348, 71.0, 71.0, 0.4446, 73.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 2.00, 324.348, 335.954, 71.0, 72.0, 0.6051, 73.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [15.0, 2.00, 335.954, 347.583, 72.0, 72.0, 0.6051, 73.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        
    # Guardamos la estructura completa en la tabla de la memoria
    st.session_state.df_corridas = pd.DataFrame(datos_muestra, columns=columnas)
    
    # Forzamos a que el índice de las filas de la muestra empiece en 1
    st.session_state.df_corridas.index = range(1, 9)