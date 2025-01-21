
from twilio.rest import Client
import numpy as np
import time
import os
from datetime import datetime
import subprocess
def enviar_mensaje_sms( ahora):
    mensaje=f"prueba a las {ahora} https://modular-2025.web.app/"
    numero_destino="+523340511109"
    account_sid = ""
    auth_token = ""
    twilio_phone_number = "+12313778984"  # e teléfono de Twilio

    # Inicializar el cliente de Twilio
    client = Client(account_sid, auth_token)

    try:
        # enviar SMS
        message = client.messages.create(
            body=mensaje,               
            from_=twilio_phone_number,  
            to=numero_destino           
        )
        print(f" enviado exitosamente. SID: {message.sid}")
        return False
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")


    try:
        subprocess.run(["firebase", "deploy"], check=True)
        print("Firebase deploy ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar firebase deploy: {e}")

    #try:
     #   os.system("python send_alert.py")
        #ejecutar seed.js
