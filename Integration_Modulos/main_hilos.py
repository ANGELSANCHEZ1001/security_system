import cv2
import numpy as np
import time
import os
import threading
import matplotlib.pyplot as plt
import sys
sys.path.append('C:/Users/angel/Desktop/CUCEI/INCO 9/Modular/codigo/modular_project/Integration_Modulos')
from send_alert import enviar_correo
from evaluate_images import predecir
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from datetime import datetime

NUM_CAPTURES = 5
SAVE_PATH = r"C:\\Users\\angel\\Desktop\\CUCEI\\INCO 9\\Modular\\codigo\\modular_project\\integration\\imagenes"
captures_taken = 0  
motion_start_time = None
show_motion = True
is_prediction_in_progress = False  # Flag to track if prediction is in progress


def predecir_imagenes():
    global captures_taken
    global NUM_CAPTURES
    human = predecir()
    print(f"ESTO ES {human}")
    return human


def detectar():
    global captures_taken
    global motion_start_time
    global show_motion
    global is_prediction_in_progress
    data_dir = r"C:\\Users\\angel\\Desktop\\CUCEI\\INCO 9\\Modular\\codigo\\modular_project\\integration\\imagenes"
    file_name = "imagen1.jpg"
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, file_name)

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not video.isOpened():
        print("Error: No se puede abrir la cámara.")
        exit()

    rectangles = []
    selected_rect = None

    start_time = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                x1, y1, w, h = cv2.boundingRect(approx)
                x2, y2 = x1 + w, y1 + h
                rectangles.append((x1, y1, x2, y2))

        cv2.imshow('Frame', frame)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            break

        height, width, _ = frame.shape
        third_width = width // 3

        def sort_rects(rects):
            return sorted(rects, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]), reverse=True)

        rects_plane1 = [r for r in rectangles if r[0] < third_width]
        rects_plane2 = [r for r in rectangles if third_width <= r[0] < 2 * third_width]
        rects_plane3 = [r for r in rectangles if r[0] >= 2 * third_width]

        rects_plane1 = sort_rects(rects_plane1)
        rects_plane2 = sort_rects(rects_plane2)
        rects_plane3 = sort_rects(rects_plane3)

        rectangles = []
        if rects_plane1: rectangles.append(rects_plane1[0])
        if rects_plane2: rectangles.append(rects_plane2[0])
        if rects_plane3: rectangles.append(rects_plane3[0])

        for i, rect in enumerate(rectangles):
            x1, y1, x2, y2 = rect
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{i + 1}", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow('Frame', frame)
        cv2.waitKey(0)

        user_input = int(input("Seleccione el número del rectángulo que desea (1-3): "))
        if 1 <= user_input <= 3:
            selected_rect = rectangles[user_input - 1]

        if selected_rect:
            x1, y1, x2, y2 = selected_rect
            rect_width = x2 - x1
            rect_height = y2 - y1
            print(f"Dimensiones del área seleccionada: {rect_width}x{rect_height} píxeles")
            print("Esperando 5 segundos antes de comenzar la detección...")
            time.sleep(5)

        i = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break

            if selected_rect:
                x1, y1, x2, y2 = selected_rect
                roi = frame[y1:y2, x1:x2]
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                if i == 20:
                    bgGray = gray_roi
                if i > 20:
                    dif = cv2.absdiff(gray_roi, bgGray)
                    _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
                    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    cv2.imshow('th', th)

                    motion_detected = False
                    for c in cnts:
                        x, y, w, h = cv2.boundingRect(c)
                        min_width = int(0.1 * rect_width)
                        min_height = int(0.1 * rect_height)

                        if w >= min_width and h >= min_height:
                            if show_motion:
                                # Mostrar área verde cuando hay movimiento
                                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), (0, 255, 0), 2)
                            motion_detected = True

                    if motion_detected:
                        if motion_start_time is None:
                            motion_start_time = time.time()
                        elif time.time() - motion_start_time >= 3:
                            if not is_prediction_in_progress:  # Ensure prediction is not already in progress
                                if captures_taken < NUM_CAPTURES:
                                    show_motion = False
                                    cv2.waitKey(1)
                                    time.sleep(1)
                                    for _ in range(NUM_CAPTURES):
                                        ret, frame = video.read()
                                        if not ret:
                                            print("No se pudo capturar un nuevo cuadro. Fin del video.")
                                            break
                                        capture_path = f"{SAVE_PATH}\\imagen{captures_taken + 1}.jpg"
                                        cv2.imwrite(capture_path, frame)
                                        print(f"Imagen guardada en: {capture_path}")
                                        captures_taken += 1
                                        time.sleep(1)

                                # Start the prediction in a new thread
                                is_prediction_in_progress = True
                                threading.Thread(target=predecir_imagenes).start()
                                time.sleep(5)
                    else:
                        motion_start_time = None
                i += 1

                # Mostrar siempre el rectángulo rojo alrededor del área seleccionada
                if selected_rect:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

detectar()
