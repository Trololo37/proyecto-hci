import voiceDetector
import gestos
import serial, time
import threading

class Main:
    def __init__(self):
        self.ser = serial.Serial('COM3', baudrate=115200, timeout=10)
        time.sleep(3)
        self.valores = []
        self.deteccion_por_voz = voiceDetector.voiceDetector()
        self.deteccion_por_imagen = gestos.gestos()
        self.detener_deteccion = False  # Variable para detener la detección
        self.esperarComando = True
        self.esperarSeleccionDeLuz = False
        self.esperarValor = False

    def send_command(self, command):
        self.ser.write((command + '\n').encode('utf-8')) 
        print(f"Comando enviado: {command}")
        time.sleep(0.3)
        response = self.ser.read_all().decode('utf-8').strip()
        if response:
            print(f"Respuesta de las luces: {response}")
        else:
            print("No se recibió una respuesta.")

    def escalator(self, value):
        mapped_value = value * (255 / 3)
        return int(mapped_value)

    def wrapper(self, tipo: str):
        if tipo == "comando":
            return self.deteccion_por_voz.esperandoComando()
        elif tipo == "luz":
            return self.deteccion_por_voz.esperandoSeleccionDeLuz()
        elif tipo == "valor":
            return self.deteccion_por_imagen.ejecutar()
        return None

    def procesar_voz(self):
        while not self.detener_deteccion:
            if self.esperarComando:
                self.esperarComando = False
                self.valores.clear()
                print("Esperando comando...")
                resultado_voz = self.wrapper("comando")
                if resultado_voz == 'luces':
                    self.esperarSeleccionDeLuz = True
                else:
                    print("Nos vemos!")
                    self.detener_deteccion = True
                    break

            if self.esperarSeleccionDeLuz:
                self.esperarSeleccionDeLuz = False
                print("Esperando accion...")
                resultado_voz = self.wrapper("luz")
                
                if resultado_voz == 'confirmar':
                    self.esperarComando = True
                    self.esperarValor = False
                    self.valores.clear()
                elif resultado_voz == 'cancelar':
                    self.esperarComando = True
                    self.esperarValor = False
                    self.valores.clear()
                elif resultado_voz == '0':
                    for i in range(1, 5):
                        command = f"{str(i)} {'0'}"
                        self.send_command(command)
                    self.esperarComando = True
                    self.esperarValor = False
                    self.valores.clear()
                    continue
                else:
                    self.esperarValor = True
                    self.esperarSeleccionDeLuz = True
                    self.valores=[resultado_voz]

    def procesar_imagen(self):
        while not self.detener_deteccion:
            if self.esperarValor:
                # print("Iniciando detección por imagen...")
                resultado_imagen = self.wrapper("valor")
                if resultado_imagen not in ['0','1','2','3','4']:
                    continue
                if len(self.valores) > 0:
                    self.valores=[self.valores[0],resultado_imagen]
                if len(self.valores) > 1:
                    if self.valores[0] == '0':
                        command = '1 0'
                    else:
                        command = f"{self.valores[0]} {self.escalator(int(self.valores[1]))}"
                    self.send_command(command)


    def main(self):

        try:
            # Iniciar los hilos para procesar voz e imagen
            hilo_voz = threading.Thread(target=self.procesar_voz)
            hilo_imagen = threading.Thread(target=self.procesar_imagen)

            # Iniciar los hilos
            hilo_voz.start()
            hilo_imagen.start()

            # Esperar que ambos hilos terminen
            hilo_voz.join()
            hilo_imagen.join()

        except KeyboardInterrupt:
            print("Ejecución interrumpida por el usuario.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.deteccion_por_imagen.ret.release()
            self.detener_deteccion=True
            self.ser.close()
            print("Ejecución terminada.")

if __name__ == '__main__':
    ejecucion = Main()
    ejecucion.main()
