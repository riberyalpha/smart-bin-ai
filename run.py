import cv2
from app.connect_to_api import send_data_to_api
from app.identify_objeto import identify_objeto

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        identificador, objetos, clasificacion = identify_objeto(frame)
        cv2.imshow("Objetos", identificador)
                
        # Enviar comandos a API
        if clasificacion['Organico']:
            send_data_to_api('Organico')
        elif clasificacion['Inorganico']:
            send_data_to_api('Inorganico')

        # Salir de la camara si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Cámara cerrada.")

if __name__ == "__main__":
    main()
