
import cv2
import time

class EyeDetector:
    def __init__(self):
        # Cargar los clasificadores en cascada para rostros y ojos
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        
        # Variables para el retardo temporal
        self.ultima_deteccion_ojos = time.time()
        """Retardo en segundos para marcar los ojos como cerrados asi evitamos que el parpadeo sea detectado como que los ojos estan cerrados"""
        self.retardo_cierre = 1  

    def detect_eyes(self, frame):
        # Convertir el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en el frame
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # Lista para almacenar el estado de los ojos (abiertos o cerrados)
        eye_states = []

        for (x, y, w, h) in faces:
            # Recortar la región de interés (ROI) para los ojos
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Detectar ojos en la ROI
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            # Determinar si los ojos están abiertos o cerrados
            if len(eyes) == 0:
                # Si no se detectan ojos, verificar si ha pasado el retardo
                if time.time() - self.ultima_deteccion_ojos >= self.retardo_cierre:
                    eye_states.append("Cerrados")
            else:
                # Si se detectan ojos, actualizar el tiempo de la última detección
                self.ultima_deteccion_ojos = time.time()
                eye_states.append("Abiertos")

            # Dibujar rectángulos alrededor de los ojos detectados (opcional)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        return eye_states
