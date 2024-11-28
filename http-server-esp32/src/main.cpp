#include <WiFi.h>
#include <WebServer.h>
#include <map>
#include <Arduino.h>
#include <esp32-hal-gpio.h>

const char *ssid = "tu_red";        // Cambia esto por tu red WiFi
const char *password = "password"; // Cambia esto por tu contraseña WiFi

WebServer server(80);

// Mapa de focos: Identificador -> Pin GPIO
std::map<String, int> focos = {
    {"foco1", 16},
    {"foco2", 17},
    {"foco3", 18},
    {"foco4", 19}};

// Luminosidad por foco (0-25)
std::map<String, int> luminosidades = {
    {"foco1", 25},
    {"foco2", 25},
    {"foco3", 25},
    {"foco4", 25}};

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
void prender();
void apagar();

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
  server.on("/prender", HTTP_POST, prender);
  server.on("/apagar", HTTP_POST, apagar);
  server.on("/luminosidad", HTTP_POST, cambiarLuminosidad);

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop()
{
  server.handleClient();
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

// Prender foco
void prender()
{
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
  String foco = obtenerFoco();
  if (foco != "" && focos.count(foco))
  {
    if (server.hasArg("valor"))
    {
      int valor = server.arg("valor").toInt();
      if (valor >= 0 && valor <= 25)
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
