import streamlit as st

@st.dialog("Teoría del sistema", width="large")
def teoria():
    
    st.header("Fundamentos del Cálculo (EPA)")
    st.markdown("""
    ### 1. La Ecuación Teórica del $\Delta H_@$
    Según el documento técnico de la EPA, la ecuación primaria (Ecuación 1) define el comportamiento del orificio basándose en la caída de presión, temperaturas y caudales teóricos:
    """)
    st.latex(r"\Delta H_@ = \frac{0.0319 \  \Delta H}{P_{bar}(t_0 + 460)} \left[ \frac{(t_w+460) \ \theta}{V_w} \right]^2")
    st.markdown("""
    dnde las condiciones de referencia para $ΔH$ se eligieron como 0,75 $dcfm$ de aire a 68 $F$ y 29,92 $in.Hg$. De estos valores surge la constante ya que
    """)
    st.latex(r"\frac{0.75^2 \ 29.92}{68+460} = 0.031875 \sim 0.0319.")
    st.markdown("""
    Nota: el manual *Maintenance Calibration And Operation Of Isokinetic Source-sampling Equipment* utiliza una constante levemente distinta porque trabaja a 70 $F$ en vez 
    de 68 $F$.      
    """)
    st.markdown("""
    **Fuentes:** 
    * [TID-001: Derivation of $\Delta H_@$ for Orifice Meters (EPA)](https://www.epa.gov/sites/default/files/2020-08/documents/tid-01.pdf)
    * [Maintenance Calibration And Operation Of Isokinetic Source-sampling Equipment, Página 12 (20 virtual)](https://nepis.epa.gov/Exe/ZyNET.exe/20013PMH.txt?ZyActionD=ZyDocument&Client=EPA&Index=Prior%20to%201976&Docs=&Query=&Time=&EndTime=&SearchMethod=1&TocRestrict=n&Toc=&TocEntry=&QField=&QFieldYear=&QFieldMonth=&QFieldDay=&UseQField=&IntQFieldOp=0&ExtQFieldOp=0&XmlQuery=&File=D%3A%5CZYFILES%5CINDEX%20DATA%5C70THRU75%5CTXT%5C00000005%5C20013PMH.txt&User=ANONYMOUS&Password=anonymous&SortMethod=h%7C-&MaximumDocuments=1&FuzzyDegree=0&ImageQuality=r75g8/r75g8/x150y150g16/i425&Display=hpfr&DefSeekPage=&SearchBack=ZyActionL&Back=ZyActionS&BackDesc=Results%20page&MaximumPages=1&ZyEntry=2#)
    """)

    st.markdown("---")

    st.markdown("""
    ### 2. Factor de Calibración de la Consola ($Y$) mediante el coeficiente de orificio $K'$
    El factor $Y$ compara el volumen medido por el patrón húmedo frente al volumen de la consola, ajustado por presiones y **temperaturas absolutas**.
    """)

    st.latex(r"Y = \frac{V_{cr(sdt)}}{V_{m(sdt)}} = \frac{K' P_{bar} \theta}{\sqrt{T_{amb}}}\frac{T_m}{K_1 V_m (P_{bar}+\frac{Delta h}{13.6})}")
    st.markdown("""
    donde $K_1= T_{(std)}/P_{(std)}$.
    """)

    st.markdown("""
    **Fuente:** 
    * [Appendix A-3 to Part 60—Test, Método 5, Sección 12.3](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-3%20to%20Part%2060)
    """)

    st.markdown("---")

    st.markdown("""
    ### 3. Unidades
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Sistema Imperial:**
        * Volumen en pies cúbicos ($ft^3$)
        * Presión en pulgadas de mercurio ($in. Hg$)
        * Presión en el orificio en pulgadas de agua ($in. H_2O$)
        * Temperatura Absoluta en Rankine: $^\circ R = ^\circ F + 460$
        * Constante EPA: **0.0319**
        """) 

    with col2:
        st.markdown("""
        **Sistema Internacional:**
        * Volumen en metros cúbicos ($m^3$)
        * Presión en milímetros de mercurio ($mm Hg$) 
        * Presión en el orificio en $mm H_2O$
        * Temperatura Absoluta en Kelvin: $K = ^\circ C + 273.15$
        * Constante Convertida: **0.0011695**
        """)

    with col3:
        st.markdown("""
        **Factores de conversión**
        * 35.3147 $ft^3$ = $m^3$
        * $in. Hg$ = 25.4 $mm Hg$
        * $in. H_2O$ = 25.4 $mm H_2O$
        """)

    st.markdown("---")

    st.markdown("""
    ### 4. Otras consideraciones
    """)

    col_tem, col_med, col_error = st.columns(3)

    with col_tem:
        st.markdown("""
        ### Temperatura 
        La normativa exige el uso de la temperatura absoluta promedio del medidor de gas.
        """)

        st.latex(r"T_m = \frac{T_{m(entrada)} + T_{m(salida)}}{2}")

    with col_med:
        st.markdown("""
        ### Mediciones 
        La normativa exige promediar al menos tres muestras.
        """)

    with col_error:
        st.markdown("""
        ### Errores propios de la reglamentación 
        A los errores de truncamiento se suma que la EPA exige ajustar la temperatura sumando 460 a los grados Fahrenheit, mientras que el cero absoluto real es -459.67.    
        """)
        
    st.markdown("""
    **Fuentes:** 
    * [40 CFR Parte 60, Apéndice A-3, Método 5, Sección 12.1](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-3%20to%20Part%2060)
    * [60.8 Performance tests, (f)](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/subpart-A/section-60.8)
    * [TID-001: Derivation of $\Delta H_@$ for Orifice Meters (EPA)](https://www.epa.gov/sites/default/files/2020-08/documents/tid-01.pdf)
    """)