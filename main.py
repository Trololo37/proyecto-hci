import serial
import time

# Configuración del puerto serial
ser = serial.Serial('COM4', baudrate=115200, timeout=10)   # Cambia COM4 por el puerto correcto
time.sleep(2)  # Espera a que el puerto serial esté listo

def send_command(command):
    """
    Envía un comando al ESP32 por el puerto serial y espera una respuesta.
    """
    ser.write((command + '\n').encode('utf-8'))  # Envía el comando al ESP32
    print(f"Command sent: {command}")
    time.sleep(1)  # Espera un momento para que el ESP32 procese el comando
    response = ser.read_all().decode('utf-8').strip()  # Lee la respuesta del ESP32
    if response:
        print(f"Response from ESP32: {response}")
    else:
        print("No response received.")

try:
    while True:
        print("\nOptions:")
        print("1: Turn on LED 1")
        print("2: Turn on LED 2")
        print("3: Turn on LED 3")
        print("4: Turn on LED 4")
        print("q: Quit")

        user_input = input("Enter your choice: ").strip()

        if user_input in ['1', '2', '3', '4']:
            send_command(user_input)  # Enviar el comando al ESP32
        elif user_input.lower() == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    ser.close()  # Cierra el puerto serial al terminar


    #
    #esptool --chip esp32s3 --port COM4 erase_flash
    #esptool --chip esp32s3 --port COM4 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin
    #
