import webbrowser
import speech_recognition as sr
import serial
import time
import os

# Configuración del puerto serial
ser = serial.Serial('COM4', baudrate=115200, timeout=10)   # Cambia COM4 por el puerto correcto
time.sleep(2)  # Espera a que el puerto serial esté listo
r = sr.Recognizer() 

    #
    #esptool --chip esp32s3 --port COM4 erase_flash
    #esptool --chip esp32s3 --port COM4 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin
    #

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

def nombre_a_numero(palabra):
    nombres_a_numeros = {
        "uno": '1',
        "dos": '2',
        "tres": '3',
        "cuatro": '4'
    }
    print(nombres_a_numeros.get(palabra.lower(), "Número no reconocido"))
    return nombres_a_numeros.get(palabra.lower(), "Número no reconocido")


while True:
    try:
        with sr.Microphone() as source:
            print('Hola, soy tu asistente por voz: ')
            print("Elige entre decir uno, dos, tres o cuatro")
            print("para prender los distintos focos, o di salir")
            time.sleep(0.5)
            print("\ndilo ahora")
            audio = r.listen(source)
            #time.sleep(0.5)
            try:
                print("traduciendo")
                text = r.recognize_google(audio, language="es")
                print('Has dicho: {}'.format(text))
                print(text)

                user_input = str(text).strip()
                print(user_input)

                texto = nombre_a_numero(user_input)

                if texto in ['1', '2', '3', '4']:
                    send_command(texto)  # Enviar el comando al ESP32
                elif text.strip()=="salir":
                    ser.close()
                    break

        #        if "luces" in text:
         #           print("Escuchando luces")
          #      if "confirmar" in text:
           #         print("Confirmar cambios")
            #    if "cancelar" in text:
             #       print("Cancelar cambios")
            except:
                print('No te he entendido')
            time.sleep(0.5)
            os.system('cls' if os.name=='nt' else 'clear')
    except KeyboardInterrupt:
        print("Cancelacion con teclado")
        break
    finally:
        ser.close()  # Cierra el puerto serial al terminar
