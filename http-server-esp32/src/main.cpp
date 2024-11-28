#include <WiFi.h>
#include <WebServer.h>
#include <map>
#include <Arduino.h>
#include <esp32-hal-gpio.h>

const char *ssid = "Fam. Gonzaminguez";        // Cambia esto por tu red WiFi
const char *password = "Fe18Ad24Da30Al17Lu01"; // Cambia esto por tu contraseña WiFi

WebServer server(80);

// Mapa de focos: Identificador -> Pin GPIO
std::map<String, int> focos = {
    {"foco1", 16},
    {"foco2", 17},
    {"foco3", 18},
    {"foco4", 19}};

// Luminosidad por foco (0-255)
std::map<String, int> luminosidades = {
    {"foco1", 255},
    {"foco2", 255},
    {"foco3", 255},
    {"foco4", 255}};

// Canales de PWM para cada foco
std::map<String, int> canalesPWM = {
    {"foco1", 0},
    {"foco2", 1},
    {"foco3", 2},
    {"foco4", 3}};

const int frecuenciaPWM = 5000; // Frecuencia del PWM en Hz
const int resolucionPWM = 8;    // Resolución del PWM (0-25)

String obtenerFoco();
void cambiarLuminosidad();
void encender();
void apagar();
void agregarCabecerasCORS();

void setup()
{
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Conectando al WiFi...");
  }

  Serial.println("WiFi conectado");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configurar pines y canales PWM
  for (auto &foco : focos)
  {
    ledcSetup(canalesPWM[foco.first], frecuenciaPWM, resolucionPWM);
    ledcAttachPin(foco.second, canalesPWM[foco.first]);
    ledcWrite(canalesPWM[foco.first], luminosidades[foco.first]); // Luminosidad inicial
  }

  // Configurar rutas
  server.on("/encender", HTTP_POST, encender);
  server.on("/apagar", HTTP_POST, apagar);
  server.on("/luminosidad", HTTP_POST, cambiarLuminosidad);

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop()
{
  server.handleClient();
}
void agregarCabecerasCORS()
{
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}

// Función auxiliar para obtener el identificador del foco
String obtenerFoco()
{
  if (server.hasArg("foco"))
  {
    return server.arg("foco");
  }
  server.send(400, "text/plain", "Falta el identificador del foco");
  return "";
}

// encender foco
void encender()
{
  agregarCabecerasCORS();
  String foco = obtenerFoco();
  if (foco != "" && focos.count(foco))
  {
    ledcWrite(canalesPWM[foco], luminosidades[foco]); // Recupera la luminosidad previa
    server.send(200, "text/plain", "Foco prendido: " + foco);
    Serial.println("Foco prendido: " + foco);
  }
  else
  {
    server.send(404, "text/plain", "Foco no encontrado");
    Serial.println("Foco no encontrado: " + foco);
  }
}

// Apagar foco
void apagar()
{
  agregarCabecerasCORS();
  String foco = obtenerFoco();
  if (foco != "" && focos.count(foco))
  {
    ledcWrite(canalesPWM[foco], 0); // Apaga el foco
    server.send(200, "text/plain", "Foco apagado: " + foco);
    Serial.println("Foco apagado: " + foco);
  }
  else
  {
    server.send(404, "text/plain", "Foco no encontrado");
    Serial.println("Foco no encontrado: " + foco);
  }
}

// Cambiar luminosidad
void cambiarLuminosidad()
{
  agregarCabecerasCORS();
  String foco = obtenerFoco();
  if (foco != "" && focos.count(foco))
  {
    if (server.hasArg("valor"))
    {
      int valor = server.arg("valor").toInt();
      if (valor >= 0 && valor <= 255)
      {
        luminosidades[foco] = valor;
        ledcWrite(canalesPWM[foco], valor);
        server.send(200, "text/plain", "Luminosidad cambiada: " + foco + " -> " + String(valor));
        Serial.println("Luminosidad cambiada: " + String(valor));
      }
      else
      {
        server.send(400, "text/plain", "Valor de luminosidad inválido");
        Serial.println("Luminosidad no valida: " + String(valor));
      }
    }
    else
    {
      server.send(400, "text/plain", "Falta el valor de luminosidad");
      Serial.println("Luminosidad faltante. ");
    }
  }
  else
  {
    server.send(404, "text/plain", "Foco no encontrado");
    Serial.println("Foco no encontrado: " + foco);
  }
}
