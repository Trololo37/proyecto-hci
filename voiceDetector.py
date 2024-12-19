import webbrowser
import speech_recognition as sr
import serial
import time
import os


class voiceDetector():
    def __init__(self):
        self.r = sr.Recognizer() 
        time.sleep(0.5)
        self.state='inactive'
    
    def nombre_a_numero(self, palabra):
        nombres_a_numeros = {
            "cero": '0',
            "uno": '1',
            "dos": '2',
            "tres": '3',
            "cuatro": '4',
        }
        return nombres_a_numeros.get(palabra.lower(), "Número no reconocido")
    
    def esperandoComando(self):
        print("Di LUCES")
        while True:
            try:
                with sr.Microphone() as source:
                    # print("\nDilo ahora")
                    audio = self.r.listen(source)
                    try:
                        # print("\n\nComando introducido")
                        text = self.r.recognize_google(audio, language="es")
                        print('Has dicho: {}'.format(text))
                        user_input = str(text).strip()
                    except Exception as e:
                        print('No logro entenderte')
                        continue
                        
                    if 'luces' in user_input.lower(): 
                        return 'luces'
                    
            except KeyboardInterrupt:
                print("Cancelacion con teclado")
                break 
        print("Cancelacion por voz")    

    def esperandoSeleccionDeLuz(self):
        print("Focos disponibles:")
        print("1) UNO")
        print("2) DOS")
        print("3) TRES")
        print("4) CUATRO")
        print("Comandos:")
        print("APAGAR TODOS")
        print("CONFIRMAR")
        print("CANCELAR")
        while True:
            try:
                with sr.Microphone() as source:
                    
                    # print("\nDilo ahora")
                    audio = self.r.listen(source)
                    try:
                        # print("\n\nComando introducido")
                        text = self.r.recognize_google(audio, language="es")
                        print('Has dicho: {}'.format(text))
                        user_input = str(text).strip()
                    except Exception as e:
                        print('No logro entenderte')
                        continue
                    
                    if 'confirmar' in user_input.lower(): 
                        return 'confirmar'
                    elif 'cancelar' in user_input.lower(): 
                        return 'cancelar'
                    
                    texto = self.nombre_a_numero(user_input)
                    time.sleep(0.5)

                    if texto in ['1', '2', '3', '4']:
                        return texto
                    elif "uno" in text.lower() or '1' in text.lower():
                        return '1'
                    elif "apagar" in text.lower() and "todos" in text.lower():
                        return '0'
                    elif "dos" in text.lower() or '2' in text.lower():
                        return '2'
                    elif "tres" in text.lower() or '3' in text.lower():
                        return '3'
                    elif "cuatro" in text.lower() or '4' in text.lower():
                        return '4'
                    elif text.strip()=="salir":
                        break
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                print("Cancelacion con teclado")
                break 
        print("La detección por voz fue cancelada")       

#if __name__ == '__main__':
#    x = voiceDetector()
#    x.ejecutar()