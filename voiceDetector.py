import webbrowser
import speech_recognition as sr
r = sr.Recognizer() 
while True:
    with sr.Microphone() as source:
        print('Hola, soy tu asistente por voz: ')
        audio = r.listen(source)
 
        try:
            text = r.recognize_google(audio, language="es")
            print('Has dicho: {}'.format(text))
            print(text)
            if "luces" in text:
                print("Escuchando luces")
            if "confirmar" in text:
                print("Confirmar cambios")
            if "cancelar" in text:
                print("Cancelar cambios")
        except:
            print('No te he entendido')