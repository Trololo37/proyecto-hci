import webbrowser
import speech_recognition as sr
import serial
import time
import os


class voiceDetector():
    def __init__(self):
        self.r = sr.Recognizer() 
        time.sleep(0.5)

    def nombre_a_numero(self, palabra):
        nombres_a_numeros = {
            "uno": '1',
            "dos": '2',
            "tres": '3',
            "cuatro": '4',
        }
        return nombres_a_numeros.get(palabra.lower(), "Número no reconocido")

    def ejecutar(self):

        while True:
            try:
                with sr.Microphone() as source:
                    print('\nHola, soy tu asistente por voz: ')
                    print("Elige entre decir uno, dos, tres o cuatro")
                    print("para prender los distintos focos, o di salir")
                    print("Ahora, espera la señal :)")
                    time.sleep(1.5)
                    print("\nDilo ahora")
                    audio = self.r.listen(source)
                    try:
                        print("\n\nTraduciendo")
                        text = self.r.recognize_google(audio, language="es")
                        print('Has dicho: {}'.format(text))
                        user_input = str(text).strip()
                        texto = self.nombre_a_numero(user_input)
                        time.sleep(0.5)

                        if texto in ['1', '2', '3', '4']:
                            return texto
                        elif "uno" in text or '1' in text:
                            return '1'
                        elif "dos" in text or '2' in text:
                            return '2'
                        elif "tres" in text or '3' in text:
                            return '3'
                        elif "cuatro" in text or '4' in text:
                            return '4'
                        elif text.strip()=="salir":
                            break
                    except Exception as e:
                        print('No te he entendido')
                        print(e)
                    time.sleep(0.1)
                    #os.system('cls' if os.name=='nt' else 'clear')
            except KeyboardInterrupt:
                print("Cancelacion con teclado")
                break 
        print("La detección por voz fue cancelada")       
