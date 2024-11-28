/**********************************************************************
  Filename    : SerialRW_LedControl
  Description : Use UART to control LEDs brightness via serial commands.
**********************************************************************/
#include <Arduino.h>

String inputString = "";      // Almacena el comando recibido
bool stringComplete = false;  // Indica si el comando está completo

// Pines de los LEDs
const int ledPins[] = {2, 4, 6, 5};  // Cambia estos valores según tu configuración
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);

void setup() {
  // Inicializa el puerto serial
  Serial.begin(115200);
  Serial.println(String("\nESP32 LED Brightness Controller Initialized!\r\n")
                 + String("Send '<LED> <BRIGHTNESS>' to control LEDs.\r\n")
                 + String("Example: '2 128' to set LED 2 to half brightness.\r\n"));

  // Configura los pines de los LEDs como salida
  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  // Apaga todos los LEDs al inicio
  }
}

void loop() {
  // Procesar entrada serial
  if (Serial.available()) {  
    char inChar = Serial.read();   // Lee un carácter
    inputString += inChar;
    if (inChar == '\n') {          // Comando completo
      stringComplete = true;
    }
  }

  if (stringComplete) {
    inputString.trim();            // Limpia espacios al inicio y final
    handleCommand(inputString);    // Procesa el comando recibido
    inputString = "";              // Limpia el comando
    stringComplete = false;        // Resetea el indicador
  }
}

// Procesa el comando recibido y controla los LEDs
void handleCommand(String command) {
  // Divide el comando en LED e intensidad
  int spaceIndex = command.indexOf(' ');
  if (spaceIndex == -1) {
    Serial.println("Invalid command format. Use '<LED> <BRIGHTNESS>'.");
    return;
  }

  String ledPart = command.substring(0, spaceIndex);
  String brightnessPart = command.substring(spaceIndex + 1);

  int ledIndex = ledPart.toInt() - 1;          // Convierte a índice (0 basado)
  int brightness = brightnessPart.toInt();    // Convierte a entero

  // Verifica que el LED y la intensidad sean válidos
  if (ledIndex >= 0 && ledIndex < ledCount && brightness >= 0 && brightness <= 255) {
    for (int i = 0; i < ledCount; i++) {
      analogWrite(ledPins[i], 0);  // Apaga todos los LEDs primero
    }
    analogWrite(ledPins[ledIndex], brightness);  // Ajusta el brillo del LED seleccionado
    Serial.printf("LED %d set to brightness %d.\r\n", ledIndex + 1, brightness);
  } else {
    Serial.println("Invalid LED number or brightness. LED: 1-4, Brightness: 0-255.");
  }
}
