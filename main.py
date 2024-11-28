#
#esptool --chip esp32s3 --port COM4 erase_flash
#esptool --chip esp32s3 --port COM4 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin
#
import voiceDetector
import gestos
import serial, time, threading

class main():
    def __init__(self):
        self.ser = serial.Serial('COM4', baudrate=115200, timeout=10)
        time.sleep(3)

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
        mapped_value =  (value) * (255/3)
        return mapped_value

    def main(self):
        while True:
            try:
                deteccion_por_voz = voiceDetector.voiceDetector()
                foco_seleccionado = deteccion_por_voz.ejecutar()
                deteccion_por_imagen = gestos.gestos()
                intensidad = deteccion_por_imagen.ejecutar()
                if foco_seleccionado and intensidad:
                    if foco_seleccionado=='0':
                        command = '1 0'
                    else:
                        command = f"{foco_seleccionado} {self.escalator(intensidad)}"
                    self.send_command(command)
            except Exception as e:
                print(e)
                if e==KeyboardInterrupt:
                    break
        self.ser.close()
        time.sleep(1)
        print("Ejecución terminada")

if __name__ == '__main__':
    ejecucion = main()
    ejecucion.main()