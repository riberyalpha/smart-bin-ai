import cv2
import numpy as np

colores = {
    'Manzana': ([0, 100, 100], [10, 255, 255]),  # HSV para el ajuste de color
    'Platano': ([20, 100, 100], [30, 255, 255]),
    'Botella': ([100, 100, 100], [130, 255, 255]),  
    'Lata': ([50, 100, 100], [70, 255, 255]) 
}

def identify_objeto(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    identificador_objeto = []
    clasificacion = {'Organico': [], 'Inorganico': []}

    for objeto, (lower, upper) in colores.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        
        mask = cv2.inRange(hsv_frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)

        # Recuadros para los contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Ignorar contornos de más
            if cv2.contourArea(contour) > 1000:
                # Aproximar el contorno a una forma más simple
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Encontrar el rectángulo delimitador del contorno
                (x, y, w, h) = cv2.boundingRect(contour)
                
                if objeto == 'Platano':
                    # Filtrar por forma (curva alargada para plátano)
                    aspect_ratio = float(w) / h
                    if 2 < aspect_ratio < 5:  # Ajustar este rango según la forma del plátano
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, objeto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        identificador_objeto.append(objeto)
                        clasificacion['Organico'].append(objeto)
                elif objeto == 'Manzana':
                    # Leer forma circular para manzana
                    aspect_ratio = float(w) / h
                    if 0.8 < aspect_ratio < 1.2:  # Añadir el rango de relación de aspecto para formas circulares
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame, objeto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        identificador_objeto.append(objeto)
                        clasificacion['Organico'].append(objeto)
                elif objeto == 'Botella' or objeto == 'Lata':
                    # Filtrar por forma (rectangular para botella y lata)
                    aspect_ratio = float(w) / h
                    if 0.5 < aspect_ratio < 2.0:  # Ajustar este rango según la forma de la botella y la lata
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.putText(frame, objeto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        identificador_objeto.append(objeto)
                        clasificacion['Inorganico'].append(objeto)
    
    return frame, identificador_objeto, clasificacion
