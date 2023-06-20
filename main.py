import cv2
import socket
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.image = Image()
        self.add_widget(self.image)

        # Inicializar la captura de video
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(
            self.update, 1.0 / 30.0
        )  # Actualizar la imagen 30 veces por segundo

        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self, dt):
        # Capturar un fotograma de la cámara
        ret, frame = self.capture.read()

        if ret:

            frame_to_send = cv2.resize(frame, (640, 480))
    
            d = frame_to_send.flatten()
            s = d.tobytes()

            for i in range(20):
                self.sock.sendto(s[i*46080:(i+1)*46080], (self.UDP_IP, self.UDP_PORT))

            # Voltear la imagen verticalmente
            frame = cv2.flip(frame, 0)

            # Convertir la imagen en formato BGR de OpenCV a formato RGB de Kivy
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Crear una textura de Kivy a partir del fotograma capturado
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="rgb"
            )
            texture.blit_buffer(frame.flatten(), colorfmt="rgb", bufferfmt="ubyte")

            # Mostrar la imagen en el widget Image
            self.image.texture = texture


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
