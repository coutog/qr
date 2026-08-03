import streamlit as st
import urllib.parse
import qrcode
import qrcode.image.svg
import io

st.set_page_config(page_title="Generador QR", page_icon="🛒")

st.title("Generador de QR")
st.write("Genera códigos QR vectoriales (100% compatibles con Illustrator) con opción de dominio personalizado.")

# 1. Selección de Dominio Base
st.subheader("1. Dominio Base")
tipo_dominio = st.radio(
    "Selecciona el origen del dominio:", 
    ["Coto (https://www.coto.com.ar/)", "Otro dominio personalizado"]
)

es_coto = "Coto" in tipo_dominio

if es_coto:
    dominio_base = "https://www.coto.com.ar/"
    ruta_url = st.text_input(
        "¿Qué sección vas a usar? (Se añadirá a https://www.coto.com.ar/)", 
        placeholder="Ej: electro / ofertas / (o déjalo en blanco)"
    )
    ruta_limpia = ruta_url.strip().lstrip("/")
    url_base = f"{dominio_base}{ruta_limpia}"
else:
    url_base = st.text_input(
        "Ingresa la URL completa del otro dominio (Sin UTMs):", 
        placeholder="Ej: https://www.midominio.com/landing"
    )

# 2. Configuración UTM (Solo visible si es Coto)
source_final = ""
if es_coto:
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
    # Validaciones básicas
    if not url_base.strip() or url_base.strip() == "https://www.coto.com.ar/":
        if es_coto and not ruta_url.strip():
            # Si es coto y la ruta está vacía, es válido (es la home)
            pass
        elif not es_coto and not url_base.strip():
            st.error("Por favor, ingresa una URL válida para el dominio personalizado.")
            st.stop()

    if es_coto and not source_final.strip():
        st.error("Por favor, ingresa o selecciona un source válido.")
        st.stop()

    # Construir URL final
    if es_coto:
        params = {
            "utm_source": source_final.strip(),
            "utm_medium": "qr",
            "utm_campaign": "ofertas"
        }
        separator = "&" if "?" in url_base else "?"
        url_final = f"{url_base}{separator}{urllib.parse.urlencode(params)}"
        sufijo_archivo = source_final.strip()
    else:
        # Dominio personalizado: se pasa la URL tal cual, sin UTMs
        url_final = url_base
        sufijo_archivo = "personalizado"

    st.success(f"**URL configurada:** {url_final}")
    
    # Generar QR vectorial en SVG (A prueba de fallos en Illustrator)
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url_final, image_factory=factory, box_size=10, border=4)
    
    buffer = io.BytesIO()
    img.save(buffer)
    
    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar QR en .SVG (Trazado Vectorial)",
        data=buffer.getvalue(),
        file_name=f"QR_{sufijo_archivo}.svg",
        mime="image/svg+xml"
    )
