import voiceDetector
import gestos
import serial, time

class Main:
    def __init__(self):
        self.ser = serial.Serial('COM4', baudrate=115200, timeout=10)
        time.sleep(3)
        self.valores = []
        self.deteccion_por_voz = voiceDetector.voiceDetector()
        self.deteccion_por_imagen = gestos.gestos()

    def send_command(self, command):
        self.ser.write((command + '\n').encode('utf-8')) 
        print(f"Command sent: {command}")
        time.sleep(0.3)
        response = self.ser.read_all().decode('utf-8').strip()
        if response:
            print(f"Response from ESP32: {response}")
        else:
            print("No response received.")

    def escalator(self, value):
        mapped_value = value * (255 / 3)
        return int(mapped_value)

    def wrapper(self, tipo: str):
        if tipo == "voz":
            return self.deteccion_por_voz.ejecutar()
        elif tipo == "imagen":
            return self.deteccion_por_imagen.ejecutar()
        return None

    def main(self):
        verificadorX=False
        verificadorY=False
        try:
            while True:
                # Paso 1: Detección por voz
                if not verificadorX:
                    verificadorX=True
                    print("Iniciando detección por voz...")
                    resultado_voz = self.wrapper("voz")
                    self.valores.append(resultado_voz)
                    

                # Paso 2: Detección por imagen
                if not verificadorY:
                    verificadorY=True
                    print("Iniciando detección por imagen...")
                    resultado_imagen = self.wrapper("imagen")
                    self.valores.append(resultado_imagen)
                    #verificadorY=True

                # Validar y enviar el comando
                if len(self.valores) > 1:
                    if self.valores[0] == '0':
                        command = '1 0'
                    else:
                        command = f"{self.valores[0]} {self.escalator(int(self.valores[1]))}"
                    self.send_command(command)
                    verificadorX=False
                    verificadorY=False

                # Limpiar valores para el siguiente ciclo
                self.valores.clear()
        except KeyboardInterrupt:
            print("Ejecución interrumpida por el usuario.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.ser.close()
            print("Ejecución terminada.")

if __name__ == '__main__':
    ejecucion = Main()
    ejecucion.main()
