import streamlit as st
import urllib.parse
import segno
import io

st.set_page_config(page_title="Generador QR", page_icon="🛒")

st.title("Generador de QR")
st.write("Genera el código QR en formato EPS con los UTMs configurados automáticamente.")

# 1. Campo para la URL / Ruta
st.subheader("1. Destino de la URL")
# st.text_input con 'placeholder' muestra el texto en gris cuando está vacío
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
        # 1. Construir URL base limpiando las barras para que no queden duplicadas
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
        
        # 3. Generar QR y guardar en memoria usando StringIO para EPS (formato de texto)
        qr = segno.make(url_final)
        buffer = io.StringIO()
        qr.save(buffer, kind='eps')
        
        # 4. Botón de descarga (convertimos el contenido del buffer de texto)
        st.download_button(
            label="⬇️ Descargar QR en .EPS",
            data=buffer.getvalue(),
            file_name=f"QR_Coto_{source_final.strip()}.eps",
            mime="application/postscript"
        )
