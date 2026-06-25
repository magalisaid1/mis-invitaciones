import pandas as pd
import webbrowser
import urllib.parse
import time

# 1. Leer el Excel
archivo = 'invitados.xlsx'
df = pd.read_excel(archivo)

# Asegurarnos de que exista la columna Estado
if 'Estado' not in df.columns:
    df['Estado'] = ''

# ---> LA LÍNEA MÁGICA QUE ARREGLA EL ERROR <---
# Le decimos a Python que la columna Estado es estrictamente de texto (string)
df['Estado'] = df['Estado'].astype(str)

print("Iniciando el asistente manual de WhatsApp...")

# 2. Recorrer cada fila
for index, row in df.iterrows():
    # Leer qué dice en la columna 'Enviar' y 'Estado'
    enviar = str(row.get('Enviar', '')).strip().lower()
    estado = str(row.get('Estado', '')).strip().lower()
    
    # Solo procesar si dice "si" en Enviar y NO dice "enviado" en Estado
    if enviar == 'si' and estado != 'enviado':
        nombre = row['Nombre']
        monto = row['Monto']
        telefono = str(row['Telefono'])
        
        if not telefono.startswith('+'):
            telefono = '+' + telefono
            
        # ---> AQUÍ ESTÁ LA CORRECCIÓN: Usamos TRES comillas (""") para textos de varias líneas
        mensaje = f"""Hola {nombre}, qué tal? 

Soy Magui del equipo de cobranzas de AD ASTRA.
Me comunico para informarle el cobro de {monto}.

Las formas de pago son:
- transferencia
- efectivo 

Alias: adastra1
CVU: 0000335100000000240541
CUIT: 20432435742
 
Por favor enviar el comprobante del pago, gracias!"""
        
        # Preparar el mensaje para internet
        mensaje_url = urllib.parse.quote(mensaje)
        
        # Crear el link mágico de WhatsApp
        link = f"https://web.whatsapp.com/send?phone={telefono}&text={mensaje_url}"
        
        print(f"\nAbriendo chat de {nombre}...")
        
        # Abrir WhatsApp Web con el mensaje ya escrito
        webbrowser.open(link)
        
        # El programa se pausa aquí
        input("👉 Ve a WhatsApp, haz clic en enviar. Luego vuelve a esta ventana negra y presiona ENTER para continuar...")
        
        # Actualiza el Excel
        df.at[index, 'Estado'] = 'Enviado'
        
        # Guarda el Excel inmediatamente
        df.to_excel(archivo, index=False)
        print(f"✅ {nombre} marcado como 'Enviado' en tu Excel.")

print("\n¡Listo! Ya revisamos toda la lista.")