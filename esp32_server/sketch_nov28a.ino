#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

// Configuración de WiFi
const char *ssid = "uach";        // Cambia esto por tu red WiFi
//const char *password = ""; // Cambia esto por tu contraseña WiFi

WebServer server(80); // Servidor web en el puerto 80

// Pines de los LEDs
const int ledPins[] = {2, 4, 6, 5}; // Cambia estos valores según tu configuración
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);

// Estado actual de los LEDs (brillo)
int ledStates[ledCount] = {0, 0, 0, 0}; // Brillo inicial (todos apagados)

String inputString = "";      // Almacena el comando recibido
bool stringComplete = false;  // Indica si el comando está completo

// Prototipos de funciones
String obtenerParametro(const String &nombre);
void manejarPrender();
void manejarApagar();
void manejarCambiarBrillo();

void setup() {
  Serial.begin(115200);

  // Configuración de pines como salida
  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
    analogWrite(ledPins[i], 0); // Inicializa todos los LEDs apagados
  }

  // Configuración de WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando al WiFi...");
  }

  Serial.println("WiFi conectado");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configuración de rutas del servidor web
  server.on("/prender", HTTP_POST, manejarPrender);
  server.on("/apagar", HTTP_POST, manejarApagar);
  server.on("/brillo", HTTP_POST, manejarCambiarBrillo);

  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop() {
  server.handleClient(); // Maneja solicitudes del cliente

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

// Obtiene un parámetro de la solicitud HTTP
String obtenerParametro(const String &nombre) {
  if (server.hasArg(nombre)) {
    return server.arg(nombre);
  }
  server.send(400, "text/plain", "Falta el parámetro: " + nombre);
  return "";
}

// Prender un LED con el brillo actual
void manejarPrender() {
  String foco = obtenerParametro("foco");
  int ledIndex = foco.toInt() - 1; // Convierte el foco a índice (0 basado)

  if (ledIndex >= 0 && ledIndex < ledCount) {
    analogWrite(ledPins[ledIndex], 255); // Usa el brillo actual
    server.send(200, "text/plain", "Foco prendido: " + foco);
    Serial.printf("Foco %d prendido con brillo %d\n", ledIndex + 1, ledStates[ledIndex]);
  } else {
    server.send(404, "text/plain", "Foco no encontrado");
  }
}

// Apagar un LED
void manejarApagar() {
  String foco = obtenerParametro("foco");
  int ledIndex = foco.toInt() - 1; // Convierte el foco a índice (0 basado)

  if (ledIndex >= 0 && ledIndex < ledCount) {
    analogWrite(ledPins[ledIndex], 0); // Apaga el LED
    server.send(200, "text/plain", "Foco apagado: " + foco);
    Serial.printf("Foco %d apagado\n", ledIndex + 1);
  } else {
    server.send(404, "text/plain", "Foco no encontrado");
  }
}

// Cambiar el brillo de un LED
void manejarCambiarBrillo() {
  String foco = obtenerParametro("foco");
  String valor = obtenerParametro("valor");

  int ledIndex = foco.toInt() - 1;    // Convierte el foco a índice (0 basado)
  int brillo = valor.toInt();         // Convierte el brillo a entero

  if (ledIndex >= 0 && ledIndex < ledCount && brillo >= 0 && brillo <= 255) {
    ledStates[ledIndex] = brillo;      // Guarda el brillo en el estado actual
    analogWrite(ledPins[ledIndex], brillo); // Cambia el brillo del LED
    server.send(200, "text/plain", "Brillo cambiado: " + foco + " -> " + String(brillo));
    Serial.printf("Brillo del foco %d cambiado a %d\n", ledIndex + 1, brillo);
  } else {
    server.send(400, "text/plain", "Foco o brillo inválido");
  }
}

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
    //for (int i = 0; i < ledCount; i++) {
    //  analogWrite(ledPins[i], 0);  // Apaga todos los LEDs primero
    //}
    analogWrite(ledPins[ledIndex], brightness);  // Ajusta el brillo del LED seleccionado
    Serial.printf("LED %d set to brightness %d.\r\n", ledIndex + 1, brightness);
  } else {
    Serial.println("Invalid LED number or brightness. LED: 1-4, Brightness: 0-255.");
  }
}

