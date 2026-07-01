# pdf_reporte.py
from fpdf import FPDF
from datetime import datetime

def generar_pdf(df_corridas, p_bar, tm_avg, y_factor, delta_h_at, unit_system):
    """Genera el reporte PDF tomando el DataFrame y devuelve los bytes listos para descargar."""
    
    # 1. Definir unidades según el sistema
    if unit_system == 'metrico':
        sistema_nombre = "sistema internacional"
        u_vol, u_temp, u_pres, u_h2o = "m3", "C", "mm Hg", "mm H2O"
    else:
        sistema_nombre = "sistema imperial"
        u_vol, u_temp, u_pres, u_h2o = "ft3", "F", "in. Hg", "in. H2O"

    # 2. Inicializar PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 3. Título y Fecha
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Reporte de calibración - EPA Método 5", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 6, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(5)
    
    # 4. Cuadro de Condiciones Generales y Resultados Finales
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 8, txt=" 1. Resultados finales y condiciones globales", ln=True, fill=True)
    
    pdf.set_font("Arial", size=10)
    pdf.ln(2)
    pdf.cell(90, 6, txt=f"Sistema de unidades: {sistema_nombre}")
    pdf.cell(100, 6, txt=f"Presión barométrica (Pbar): {p_bar:.2f} {u_pres}", ln=True)
    pdf.cell(90, 6, txt=f"Temperatura promedio salida: {tm_avg:.1f} {u_temp}")
    pdf.cell(100, 6, txt=f"Factor de calibración global (Y): {y_factor:.4f}", ln=True)
    pdf.cell(90, 6, txt="")
    pdf.cell(100, 6, txt=f"Delta H@ promedio: {delta_h_at:.4f} {u_h2o}", ln=True)
    pdf.ln(5)
    
    # 5. Tabla de Corridas Individuales
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt=" 2. Detalle de las corridas", ln=True, fill=True)
    pdf.ln(2)
    
    # Configuración de los anchos de las columnas de la tabla (Suman ~190mm)
    col_w = [8, 16, 20, 22, 22, 25, 25, 25, 27]
    headers = ["#", "t (min)", f"dH ({u_h2o})", f"Vm ({u_vol})", "K'", "Vm(std)", "Vcr(std)", "Y", f"dH@ ({u_h2o})"]
    
    # Imprimir encabezados
    pdf.set_font("Arial", 'B', 8)
    for i, head in enumerate(headers):
        pdf.cell(col_w[i], 8, txt=head, border=1, align='C')
    pdf.ln()
    
    # Imprimir filas
    pdf.set_font("Arial", size=8)
    for index, row in df_corridas.iterrows():
        # Filtramos filas vacías para que no salgan llenas de ceros en el reporte impreso
        if row['theta'] <= 0 or row['Y'] == 0:
            continue
            
        pdf.cell(col_w[0], 8, txt=str(index), border=1, align='C')
        pdf.cell(col_w[1], 8, txt=f"{row['theta']:.2f}", border=1, align='C')
        pdf.cell(col_w[2], 8, txt=f"{row['delta_h']:.2f}", border=1, align='C')
        pdf.cell(col_w[3], 8, txt=f"{row['V_m']:.3f}", border=1, align='C')
        pdf.cell(col_w[4], 8, txt=f"{row['k_prime']:.4f}", border=1, align='C')
        pdf.cell(col_w[5], 8, txt=f"{row['V_m_std']:.3f}", border=1, align='C')
        pdf.cell(col_w[6], 8, txt=f"{row['V_cr_std']:.3f}", border=1, align='C')
        pdf.cell(col_w[7], 8, txt=f"{row['Y']:.4f}", border=1, align='C')
        pdf.cell(col_w[8], 8, txt=f"{row['delta_h_at']:.4f}", border=1, align='C')
        pdf.ln()
        
    return pdf.output(dest="S").encode("latin-1")