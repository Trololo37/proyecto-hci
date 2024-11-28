import webbrowser
import speech_recognition as sr
import serial
import time
import os

ser = serial.Serial('COM4', baudrate=115200, timeout=10)
time.sleep(2.5)  
r = sr.Recognizer() 
time.sleep(0.5)

    #
    #esptool --chip esp32s3 --port COM4 erase_flash
    #esptool --chip esp32s3 --port COM4 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin
    #

def send_command(command):
    ser.write((command + '\n').encode('utf-8')) 
    print(f"Command sent: {command}")
    time.sleep(0.1)
    response = ser.read_all().decode('utf-8').strip()
    if response:
        print(f"Response from ESP32: {response}")
    else:
        print("No response received.")

def nombre_a_numero(palabra):
    nombres_a_numeros = {
        "uno": '1',
        "dos": '2',
        "tres": '3',
        "cuatro": '4',
    }
    return nombres_a_numeros.get(palabra.lower(), "Número no reconocido")


while True:
    try:
        with sr.Microphone() as source:
            print('\nHola, soy tu asistente por voz: ')
            print("Elige entre decir uno, dos, tres o cuatro")
            print("para prender los distintos focos, o di salir")
            print("Ahora, espera la señal :)")
            time.sleep(1.5)
            print("\nDilo ahora")
            audio = r.listen(source)
            try:
                print("traduciendo")
                text = r.recognize_google(audio, language="es")
                print('Has dicho: {}'.format(text))
                user_input = str(text).strip()
                texto = nombre_a_numero(user_input)
                time.sleep(0.5)

                if texto in ['1', '2', '3', '4']:
                    send_command(texto)
                    time.sleep(0.5)
                elif "uno" in text or '1' in text:
                    send_command(nombre_a_numero("uno"))
                elif "dos" in text or '2' in text:
                    send_command(nombre_a_numero("dos"))
                elif "tres" in text or '3' in text:
                    send_command(nombre_a_numero("tres"))
                elif "cuatro" in text or '4' in text:
                    send_command(nombre_a_numero("cuatro"))
                elif text.strip()=="salir":
                    ser.close()
                    break

        #        if "luces" in text:
         #           print("Escuchando luces")
          #      if "confirmar" in text:
           #         print("Confirmar cambios")
            #    if "cancelar" in text:
             #       print("Cancelar cambios")
            except Exception as e:
                print('No te he entendido')
                print(e)
            time.sleep(0.5)
            #os.system('cls' if os.name=='nt' else 'clear')
    except KeyboardInterrupt:
        print("Cancelacion con teclado")
        ser.close() 
        break        
