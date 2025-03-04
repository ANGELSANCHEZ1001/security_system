import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import cv2
from tkinter import simpledialog
import json

USER_CREDENTIALS = {"admin": "1234"}


def validar_login():
    usuario = entry_user.get()
    clave = entry_pass.get()
    
    if usuario in USER_CREDENTIALS and USER_CREDENTIALS[usuario] == clave:
        login_window.destroy()
        mostrar_menu()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def mostrar_menu():
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("600x400")
    frame_left = tk.Frame(menu, width=300, height=400, bg="white")
    frame_left.pack(side="left", fill="both")

    try:
        script_path = os.path.join(os.path.dirname(__file__), "area.jpg")
        img = Image.open(script_path)
        img = img.resize((300, 400))
        img = ImageTk.PhotoImage(img)
        label_img = tk.Label(frame_left, image=img)
        label_img.image = img
        label_img.pack()
    except Exception as e:
        label_img = tk.Label(frame_left, text="Imagen no encontrada", bg="white")
        label_img.pack()


    frame_right = tk.Frame(menu, width=300, height=400, bg="lightgray")
    frame_right.pack(side="right", fill="both", expand=True)

    botones = ["Nueva Área", "Configuracion", "Start"]
    for boton in botones:
        if boton == "Nueva Área":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=lambda: seleccionar_area(menu)).pack(pady=10)
        elif boton == "Start":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=run_main_script).pack(pady=10)
        elif boton == "Configuracion":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=settings).pack(pady=10)
        else:
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12)).pack(pady=10)

    menu.mainloop()

def run_main_script():
    script_path = os.path.join(os.path.dirname(__file__), "main_sin_show.py")
    subprocess.Popen(["python", script_path], shell=True)

def settings():
    root = tk.Tk()
    root.withdraw()  
    ip = simpledialog.askstring("Dirección IP", "Ingresa la dirección IP de la cámara (deja vacío para usar la cámara predeterminada):")

    if not ip:
        ip = "0"

    data = {"ip": ip}
    with open("camara.json", "w") as file: 
        json.dump(data, file, indent=4)


def seleccionar_area(menu):
    menu.destroy()  # Cerrar la ventana del menú

    video = cv2.VideoCapture(0)  # Cambia a la cámara deseada o usa una imagen fija

    if not video.isOpened():
        messagebox.showerror("Error", "No se pudo abrir la cámara.")
        return

    for _ in range(30):  # 3 segundos a 10 FPS
        ret, frame = video.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo leer un cuadro de la cámara.")
            video.release()
            return

    cv2.imshow('Seleccione el área de interés y presione Enter', frame)
    roi = cv2.selectROI('Seleccione el área de interés y presione Enter', frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Seleccione el área de interés y presione Enter')

    if roi == (0, 0, 0, 0):
        messagebox.showinfo("Información", "No se seleccionó un área.")
        video.release()
        return

    coordenadas = {
        "x1": roi[0],
        "y1": roi[1],
        "x2": roi[0] + roi[2],
        "y2": roi[1] + roi[3]
    }
    with open("coordenadas_area.json", "w") as archivo_json:
        json.dump(coordenadas, archivo_json)
    messagebox.showinfo("Información", "Coordenadas guardadas en 'coordenadas_area.json'.")

    # Dibujar el recuadro rojo
    imagen_con_recuadro = frame.copy()
    cv2.rectangle(imagen_con_recuadro, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 0, 255), 2)
    cv2.imwrite("./sistema/area.jpg", imagen_con_recuadro)  # Guarda la imagen con el recuadro
    messagebox.showinfo("Información", "Imagen con recuadro guardada como 'area.jpg'.")

    video.release()
    cv2.destroyAllWindows()
    mostrar_menu()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")
login_window.resizable(False, False)

bg_color = "#f0f0f0"
login_window.configure(bg=bg_color)

tk.Label(login_window, text="Usuario:", bg=bg_color, font=("Helvetica", 12)).pack(pady=10)
entry_user = tk.Entry(login_window, font=("Helvetica", 12))
entry_user.pack(pady=5)

tk.Label(login_window, text="Contraseña:", bg=bg_color, font=("Helvetica", 12)).pack(pady=10)
entry_pass = tk.Entry(login_window, show="*", font=("Helvetica", 12))
entry_pass.pack(pady=5)

tk.Button(login_window, text="Ingresar", command=validar_login, bg="#007BFF", fg="white", font=("Helvetica", 16), width=20, height=2).pack(pady=20)


login_window.update_idletasks()
width = login_window.winfo_width()
height = login_window.winfo_height()
x = (login_window.winfo_screenwidth() // 2) - (width // 2)
y = (login_window.winfo_screenheight() // 2) - (height // 2)
login_window.geometry(f"{width}x{height}+{x}+{y}")

login_window.mainloop()
