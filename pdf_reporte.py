# pdf_reporte.py
from fpdf import FPDF
from datetime import datetime

# Agregamos los parámetros entre los paréntesis para que reciba la información desde app.py
def generar_pdf(vw, tw_val, theta, vm, tm_in, tm_out, p_bar, delta_h, tm_avg, y_factor, delta_h_at, unit_system):
    """Genera el reporte PDF y devuelve los bytes listos para descargar."""
    
    # Definir etiquetas según el sistema de unidades recibido
    if unit_system == 'metrico':
        sistema_nombre = "Sistema Internacional / Argentino (Metrico)"
        u_vol, u_temp, u_pres, u_h2o = "m3", "C", "mm Hg", "mm H2O"
    else:
        sistema_nombre = "Sistema Imperial (US Customary)"
        u_vol, u_temp, u_pres, u_h2o = "ft3", "F", "in. Hg", "in. H2O"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de Calibracion - EPA Metodo 5", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    
    # Datos de entrada usando las variables que entran a la función
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Sistema de Unidades: {sistema_nombre}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=f"Volumen Patron Humedo (Vw): {vw} {u_vol}", ln=True)
    pdf.cell(200, 8, txt=f"Volumen Medidor Seco (Vm): {vm} {u_vol}", ln=True)
    pdf.cell(200, 8, txt=f"Temp. Patron Humedo (Tw): {tw_val} {u_temp}", ln=True)
    pdf.cell(200, 8, txt=f"Temp. Entrada Medidor (Tm_in): {tm_in} {u_temp}", ln=True)
    pdf.cell(200, 8, txt=f"Temp. Salida Medidor (Tm_out): {tm_out} {u_temp}", ln=True)
    pdf.cell(200, 8, txt=f"Presion Barometrica (Pbar): {p_bar} {u_pres}", ln=True)
    pdf.cell(200, 8, txt=f"Caida de Presion (Delta H): {delta_h} {u_h2o}", ln=True)
    pdf.cell(200, 8, txt=f"Tiempo de calibracion (Theta): {theta} min", ln=True)
    
    # Resultados
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Resultados del Calculo", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Temperatura Promedio (Tm): {tm_avg:.2f} {u_temp}", ln=True)
    pdf.cell(200, 10, txt=f"Factor Y: {y_factor:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Delta H@: {delta_h_at:.4f} {u_h2o}", ln=True)
    
    return pdf.output(dest="S").encode("latin-1")