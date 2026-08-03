import streamlit as st
import urllib.parse
import segno
import io

st.set_page_config(page_title="Generador QR", page_icon="🛒")

st.title("Generador de QR")
st.write("Genera el código QR con los UTMs configurados automáticamente.")

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

# 3. Formato de Exportación
st.subheader("3. Formato de descarga")
# Agregamos un selector (radio button) para que elijas el formato al momento de descargar
formato = st.radio("Elige el formato del vector:", ["SVG (Recomendado para Illustrator)", "EPS"])

# Generación
if st.button("Generar QR", type="primary"):
    if not source_final.strip():
        st.error("Por favor, ingresa un source válido.")
    else:
        # Construir URL base limpiando las barras
        dominio = "https://www.coto.com.ar/"
        ruta_limpia = ruta_url.strip().lstrip("/")
        base_url = f"{dominio}{ruta_limpia}"
        
        # Agregar parámetros UTM
        params = {
            "utm_source": source_final.strip(),
            "utm_medium": "qr",
            "utm_campaign": "ofertas"
        }
        url_final = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        st.success(f"**URL configurada:** {url_final}")
        
        # Generar QR
        qr = segno.make(url_final)
        
        # Lógica condicional: Separamos la memoria según el formato
        if "SVG" in formato:
            buffer = io.BytesIO()  # El SVG necesita memoria en Bytes
            qr.save(buffer, kind='svg', scale=10)
            file_ext = "svg"
            mime_type = "image/svg+xml"
        else:
            buffer = io.StringIO() # El EPS necesita memoria en Texto
            qr.save(buffer, kind='eps', scale=10)
            file_ext = "eps"
            mime_type = "application/postscript"
        
        # Botón de descarga dinámico
        st.download_button(
            label=f"⬇️ Descargar QR en .{file_ext.upper()}",
            data=buffer.getvalue(),
            file_name=f"QR_Coto_{source_final.strip()}.{file_ext}",
            mime=mime_type
        )
