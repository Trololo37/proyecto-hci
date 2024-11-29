#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

// Configuración de WiFi
const char *ssid = "Fam. Gonzaminguez";        // Cambia esto por tu red WiFi
const char *password = "Fe18Ad24Da30Al17Lu01"; // Cambia esto por tu contraseña WiFi

WebServer server(80); // Servidor web en el puerto 80

// Pines de los LEDs
const int ledPins[] = {13, 12, 14, 27}; // Cambia estos valores según tu configuración
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);

// Estado actual de los LEDs (brillo)
int ledStates[ledCount] = {0, 0, 0, 0}; // Brillo inicial (todos apagados)

String inputString = "";     // Almacena el comando recibido
bool stringComplete = false; // Indica si el comando está completo

// Prototipos de funciones
String obtenerParametro(const String &nombre);
void manejarPrender();
void manejarApagar();
void manejarCambiarBrillo();
void handleCommand(String command);
void manejarEstado();

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Conectando al WiFi...");
  }

  Serial.println("WiFi conectado");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configuración de pines como salida
  for (int i = 0; i < ledCount; i++)
  {
    pinMode(ledPins[i], OUTPUT);
    analogWrite(ledPins[i], 0); // Inicializa todos los LEDs apagados
  }

  // Configuración de rutas del servidor web
  server.on("/prender", HTTP_POST, manejarPrender);
  server.on("/apagar", HTTP_POST, manejarApagar);
  server.on("/brillo", HTTP_POST, manejarCambiarBrillo);
  server.on("/estado", HTTP_GET, manejarEstado);

  server.begin();
  Serial.println("Servidor web iniciado");
}

void loop()
{
  server.handleClient(); // Maneja solicitudes del cliente

  if (Serial.available())
  {
    char inChar = Serial.read(); // Lee un carácter
    inputString += inChar;
    if (inChar == '\n')
    { // Comando completo
      stringComplete = true;
    }
  }

  if (stringComplete)
  {
    inputString.trim();         // Limpia espacios al inicio y final
    handleCommand(inputString); // Procesa el comando recibido
    inputString = "";           // Limpia el comando
    stringComplete = false;     // Resetea el indicador
  }
}
void agregarCabecerasCORS()
{
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}

// Nuevo endpoint para obtener el estado de los LEDs
void manejarEstado()
{

  // Construimos el JSON con los estados de los LEDs
  String json = "{";
  for (int i = 0; i < ledCount; i++)
  {
    json += "\"" + String(i) + "\": " + String(ledStates[i]);
    if (i < ledCount - 1)
    {
      json += ", ";
    }
  }
  json += "}";

  agregarCabecerasCORS();
  Serial.println("Estado enviado");
  server.send(200, "application/json", json);
}

// Obtiene un parámetro de la solicitud HTTP
String obtenerParametro(const String &nombre)
{
  if (server.hasArg(nombre))
  {
    return server.arg(nombre);
  }
  server.send(400, "text/plain", "Falta el parámetro: " + nombre);
  return "";
}

// Prender un LED con el brillo actual
void manejarPrender()
{
  String foco = obtenerParametro("foco");
  int ledIndex = foco.toInt(); // Convierte el foco a índice (0 basado)

  agregarCabecerasCORS();
  if (ledIndex >= 0 && ledIndex < ledCount)
  {
    ledStates[ledIndex] = 255;

    analogWrite(ledPins[ledIndex], ledStates[ledIndex]); // Usa el brillo actual
    server.send(200, "text/plain", "Foco encendido: " + foco);
    Serial.printf("Foco %d encendido con brillo %d\n", ledIndex + 1, ledStates[ledIndex]);
  }
  else
  {
    server.send(404, "text/plain", "Foco no encontrado");
  }
}

// Apagar un LED
void manejarApagar()
{
  String foco = obtenerParametro("foco");
  int ledIndex = foco.toInt(); // Convierte el foco a índice (0 basado)

  agregarCabecerasCORS();
  if (ledIndex >= 0 && ledIndex < ledCount)
  {
    ledStates[ledIndex] = 0;
    analogWrite(ledPins[ledIndex], ledStates[ledIndex]); // Apaga el LED
    server.send(200, "text/plain", "Foco apagado: " + foco);
    Serial.printf("Foco %d apagado\n", ledIndex + 1);
  }
  else
  {
    server.send(404, "text/plain", "Foco no encontrado");
  }
}

// Cambiar el brillo de un LED
void manejarCambiarBrillo()
{
  String foco = obtenerParametro("foco");
  String valor = obtenerParametro("valor");

  agregarCabecerasCORS();
  int ledIndex = foco.toInt(); // Convierte el foco a índice (0 basado)
  int brillo = valor.toInt();  // Convierte el brillo a entero

  if (ledIndex >= 0 && ledIndex < ledCount && brillo >= 0 && brillo <= 255)
  {
    ledStates[ledIndex] = brillo;           // Guarda el brillo en el estado actual
    analogWrite(ledPins[ledIndex], brillo); // Cambia el brillo del LED
    server.send(200, "text/plain", "Brillo cambiado: " + foco + " -> " + String(brillo));
    Serial.printf("Brillo del foco %d cambiado a %d\n", ledIndex + 1, brillo);
  }
  else
  {
    server.send(400, "text/plain", "Foco o brillo inválido");
  }
}

void handleCommand(String command)
{
  // Divide el comando en LED e intensidad
  int spaceIndex = command.indexOf(' ');
  if (spaceIndex == -1)
  {
    Serial.println("Invalid command format. Use '<LED> <BRIGHTNESS>'.");
    return;
  }

  String ledPart = command.substring(0, spaceIndex);
  String brightnessPart = command.substring(spaceIndex + 1);

  int ledIndex = ledPart.toInt() - 1;      // Convierte a índice (0 basado)
  int brightness = brightnessPart.toInt(); // Convierte a entero

  // Verifica que el LED y la intensidad sean válidos
  if (ledIndex >= 0 && ledIndex < ledCount && brightness >= 0 && brightness <= 255)
  {
    // for (int i = 0; i < ledCount; i++) {
    //   analogWrite(ledPins[i], 0);  // Apaga todos los LEDs primero
    // }
    ledStates[ledIndex]=brightness;
    analogWrite(ledPins[ledIndex], ledStates[ledIndex]); // Ajusta el brillo del LED seleccionado
    Serial.printf("LED %d set to brightness %d.\r\n", ledIndex + 1, ledStates[ledIndex]);
  }
  else
  {
    Serial.println("Invalid LED number or brightness. LED: 1-4, Brightness: 0-255.");
  }
}
