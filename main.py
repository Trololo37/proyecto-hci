#
#esptool --chip esp32s3 --port COM4 erase_flash
#esptool --chip esp32s3 --port COM4 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin
#
import voiceDetector

self.ser = serial.Serial('COM4', baudrate=115200, timeout=10)

def send_command(command):
    ser.write((command + '\n').encode('utf-8')) 
    print(f"Command sent: {command}")
    time.sleep(0.1)
    response = ser.read_all().decode('utf-8').strip()
    if response:
        print(f"Response from ESP32: {response}")
    else:
        print("No response received.")


deteccion_por_voz = voiceDetector()
foco_seleccionado = deteccion_por_voz.ejecutar()

deteccion_por_imagen = gestos()
intensidad = deteccion_por_imagen.detectar()