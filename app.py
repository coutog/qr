import streamlit as st
import urllib.parse
import segno
import io

st.set_page_config(page_title="Generador QR Coto", page_icon="🛒")

st.title("Generador de QR - Coto")
st.write("Genera el código QR en formato EPS con los UTMs configurados automáticamente.")

# Opciones de source
opciones_source = ["tv", "flyer", "luzu", "olga", "Wanda", "revista", "camion", "Monitores", "Otro"]

# Formulario
source = st.selectbox("Selecciona el utm_source:", opciones_source)

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
        # 1. Construir URL
        base_url = "https://www.coto.com.ar/"
        params = {
            "utm_source": source_final.strip(),
            "utm_medium": "qr",
            "utm_campaign": "ofertas"
        }
        url_final = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        st.success(f"**URL configurada:** {url_final}")
        
        # 2. Generar QR y guardar en memoria usando StringIO para EPS (formato de texto)
        qr = segno.make(url_final)
        buffer = io.StringIO()
        qr.save(buffer, kind='eps')
        
        # 3. Botón de descarga (convertimos el contenido del buffer de texto)
        st.download_button(
            label="⬇️ Descargar QR en .EPS",
            data=buffer.getvalue(),
            file_name=f"QR_Coto_{source_final.strip()}.eps",
            mime="application/postscript"
        )
