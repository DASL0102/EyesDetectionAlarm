
from EyeDetector import EyeDetector
import cv2
import pygame

def main():
    # Crear una instancia de la clase EyeDetector
    eye_detector = EyeDetector()
    # Inicializar pygame
    pygame.mixer.init()
    pygame.mixer.music.load("Alarm Beeping Sound Effect.mp3")  # Cambia la ruta al archivo de sonido


    cap = cv2.VideoCapture(0)

     # Variable de control para saber si la alarma está sonando
    alarma_sonando = False
    while True:
        # Leer un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar ojos en el frame
        eye_states = eye_detector.detect_eyes(frame)
        
        
        if eye_states:
            if eye_states[0] == "Cerrados":
                if not alarma_sonando:  # Solo reproducir la alarma si no está sonando
                    pygame.mixer.music.play()
                    alarma_sonando = True  # Marcar que la alarma está sonando
                    print("Ojos cerrados - Alarma activada")
            else:
                if alarma_sonando:  # Solo detener la alarma si está sonando
                    pygame.mixer.music.stop()
                    alarma_sonando = False  # Marcar que la alarma está detenida
                    print("Ojos abiertos - Alarma detenida")

      
        for i, state in enumerate(eye_states):
            cv2.putText(frame, f"Ojos {i+1}: {state}", (10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mostrar el frame r
        cv2.imshow('Frame', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    