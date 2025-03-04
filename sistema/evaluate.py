# -*- coding: utf-8 -*-
import numpy as np
import os
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from screeninfo import get_monitors

model = load_model(r"C:\\Users\\angel\\Desktop\\CUCEI\\INCO 9\\Modular\\codigo\\modular_project\\modelo13_transfer_learning_person_InceptionV3.h5")

def predecir(save, ahora):
    count_p = 0
    classes = {0: 'gato', 1: 'perro', 2: 'persona', 3: 'puertas'}
    image_path = save
    print(f"Imagenes en el directorio: {save}")
    
    image_files = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not image_files:
        print("No se encontraron imagenes en el directorio.")
        return False

    # Obtener dimensiones de la pantalla
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height

    for image in image_files:
        full_path = os.path.join(image_path, image)
        print(f"Procesando imagen: {full_path}")
        
        image_bgr = cv2.imread(full_path)
        if image_bgr is None:
            print(f"Error al cargar la imagen: {full_path}")
            continue  # Saltar esta imagen y seguir con la siguiente

        resized_image = cv2.resize(image_bgr, (224, 224))  # Redimensionar para el modelo
        image_array = img_to_array(resized_image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array, verbose=0)[0]
        predicted_class = np.argmax(predictions)
        confidence = predictions[predicted_class] * 100
        predicted_label = classes[predicted_class]

        print(f"Prediccion: {predicted_label} ({confidence:.2f}%)")
        if predicted_label == "persona":
            count_p += 1
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5 
        thickness = 2
        color = (0, 0, 255) 
        lineas = ["Prediccion:", f"{predicted_label}", f"({confidence:.2f}%)"]
        x, y = 20, 30  # Coordenadas iniciales
        dy = 40  # Espaciado entre líneas

        for i, linea in enumerate(lineas):
            cv2.putText(image_bgr, linea, (x, y + i * dy), font, font_scale, color, thickness)

        # Obtener el tamaño de la imagen para centrarla
        height, width, _ = image_bgr.shape
        window_name = f"Prediccion: {image}"

        # Crear la ventana y centrarla
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, width, height)
        cv2.moveWindow(window_name, (screen_width - width) // 2, (screen_height - height) // 2)

        cv2.imshow(window_name, image_bgr)
        cv2.waitKey(3000)  # Mostrar 3 segundos por imagen

        print(f"Terminando prediccion {count_p}...")

        if count_p >= 3:
            cv2.destroyAllWindows()  # Cerrar la ventana de OpenCV antes de salir
            return True
    
    cv2.destroyAllWindows()  # Cerrar ventana al final del proceso
    return False
