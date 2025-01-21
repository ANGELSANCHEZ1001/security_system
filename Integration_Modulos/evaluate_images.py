import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
import cv2

import time

# Carga del modelo fuera de la func#Cambiar el path por uno dinamico o relativo
MODEL_PATH = r"C:\\Users\\angel\\Desktop\\CUCEI\\INCO 9\\Modular\\codigo\\modular_project\\modelo13_transfer_learning_person_InceptionV3.h5"
model = load_model(MODEL_PATH)
def predecir(save, ahora):
    count_p = 0
    classes = {0: 'cat', 1: 'dog', 2: 'person', 3: 'doors'}
    image_path = save
    print(f"Imagenes path: {save}")
    image_files = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    for image in image_files:
        full_path = os.path.join(image_path, image)
        print(f"Procesando la imagen: {full_path}")
        image_bgr = cv2.imread(full_path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(image_rgb, (224, 224))
        image_array = img_to_array(resized_image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array, verbose=0)[0]
        print(" % category:")
        for idx, score in enumerate(predictions):
            print(f"{classes[idx]}: {score * 100:.2f}%")
        predicted_class = np.argmax(predictions)
        confidence = predictions[predicted_class] * 100
        predicted_label = classes[predicted_class]

        print(f"Image belong to y: {predicted_label} ({confidence:.2f}%)")
        if predicted_label == "person":
            count_p += 1
        
        # Mostrar la imagen con OpenCV
        cv2.imshow(f"Predicted: {predicted_label} ({confidence:.2f}%)", image_rgb)

        # Espera por 4 segundos y luego cierra la ventana de imagen
        cv2.waitKey(3000)  # 4000 ms = 4 segundos
        cv2.destroyAllWindows()

        print(f"Finishing prediction {count_p}...")

        if count_p >= 3:
            return True
    return False
