import streamlit as st
import urllib.parse
import pyqrcode
import io

st.set_page_config(page_title="Generador QR", page_icon="🛒")

st.title("Generador de QR")
st.write("Genera el código QR en formato EPS (Vectores de relleno, ideal para Illustrator).")

# 1. Campo para la URL / Ruta
st.subheader("1. Destino de la URL")
ruta_url = st.text_input(
    "¿Qué sección vas a usar? (Se añadirá a https://www.coto.com.ar/)", 
    placeholder="Ej: electro / ofertas / (o déjalo en blanco)"
)

# 2. Origen (UTMs)
st.subheader("2. Configuración UTM")
opciones_source = ["tv", "flyer", "luzu", "olga", "Wanda", "revista", "camion", "Monitores", "Otro"]

source = st.selectbox("Selecciona en dónde vas a utilizar el QR:", opciones_source)

if source == "Otro":
    source_final = st.text_input("Ingresa el source personalizado:")
else:
    source_final = source

st.caption("Valores fijos aplicados: Medium (qr) | Campaign (ofertas)")

# Generación
if st.button("Generar QR", type="primary"):
    if not source_final.strip():
        st.error("Por favor, ingresa un source válido.")
    else:
        # 1. Construir URL base limpiando las barras
        dominio = "https://www.coto.com.ar/"
        ruta_limpia = ruta_url.strip().lstrip("/")
        base_url = f"{dominio}{ruta_limpia}"
        
        # 2. Agregar parámetros UTM
        params = {
            "utm_source": source_final.strip(),
            "utm_medium": "qr",
            "utm_campaign": "ofertas"
        }
        url_final = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        st.success(f"**URL configurada:** {url_final}")
        
        # 3. Generar QR con pyqrcode y guardar en memoria
        # Usamos error='L' (Low) que hace el QR más limpio y con menos densidad de cuadraditos
        qr = pyqrcode.create(url_final, error='L')
        buffer = io.StringIO()
        
        # Guardamos como EPS con una escala estándar base
        qr.eps(buffer, scale=10)
        
        # 4. Botón de descarga
        st.download_button(
            label="⬇️ Descargar QR en .EPS",
            data=buffer.getvalue(),
            file_name=f"QR_Coto_{source_final.strip()}.eps",
            mime="application/postscript"
        )
