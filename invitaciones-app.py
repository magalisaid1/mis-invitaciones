import streamlit as st
import pandas as pd
import urllib.parse
import io 

st.set_page_config(page_title="Invitaciones de Viaje", page_icon="✈️")
st.title("✈️ Asistente de Viaje en la Nube")
st.write("Sube tu Excel, envía los mensajes y descarga tu Excel actualizado.")

# 1. LA MEMORIA: Le decimos a la web que recuerde nuestro Excel
if 'datos' not in st.session_state:
    st.session_state.datos = None

# 2. EL BOTÓN DE SUBIDA: Para que el usuario cargue su archivo
archivo_subido = st.file_uploader("Paso 1: Sube tu archivo Excel", type=["xlsx"])

# Si hay un archivo subido y nuestra memoria está vacía, lo guardamos
if archivo_subido is not None and st.session_state.datos is None:
    df = pd.read_excel(archivo_subido)
    if 'Estado' not in df.columns:
        df['Estado'] = ''
    df['Estado'] = df['Estado'].astype(str)
    st.session_state.datos = df

# 3. SI YA TENEMOS DATOS, MOSTRAMOS TODO
if st.session_state.datos is not None:
    df = st.session_state.datos 
    
    st.write("### 📋 Tu lista actual:")
    st.dataframe(df)
    
    st.write("### 🚀 Pendientes de envío:")
    
    pendientes = 0
    for index, row in df.iterrows():
        enviar = str(row.get('Enviar', '')).strip().lower()
        estado = str(row.get('Estado', '')).strip().lower()
        
        if enviar == 'si' and estado != 'enviado':
            pendientes += 1
            nombre = row['Nombre']
            fecha = row['Fecha']
            donde = row['Donde']
            telefono = str(row['Telefono'])
            
            if not telefono.startswith('+'):
                telefono = '+' + telefono
                
            # TU MENSAJE DE VIAJE
            mensaje = f"¡Hola {nombre}! nos vamos de viaje el {fecha} a {donde}!!!!"
            
            mensaje_url = urllib.parse.quote(mensaje)
            link = f"https://web.whatsapp.com/send?phone={telefono}&text={mensaje_url}"
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.link_button(f"💬 1. Abrir WhatsApp de {nombre}", link)
            
            with col2:
                if st.button(f"✅ 2. Marcar '{nombre}' como Enviado", key=f"btn_{index}"):
                    st.session_state.datos.at[index, 'Estado'] = 'Enviado'
                    st.rerun()
                    
    if pendientes == 0:
        st.success("¡No hay mensajes pendientes!")

    # 4. EL BOTÓN DE DESCARGA
    st.write("---")
    st.write("### 💾 Guarda tu progreso:")
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        st.session_state.datos.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 Descargar Excel Actualizado",
        data=buffer.getvalue(),
        file_name="invitados_actualizado.xlsx",
        mime="application/vnd.ms-excel"
    )
