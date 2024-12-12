//BIBLIOTECAS
#include "DHT.h"

//DEFINIÇÕES
#define DHTPIN A1     
#define DHTTYPE DHT11  

//DECLARAÇÕES
DHT dht(DHTPIN, DHTTYPE);
byte prot[4];

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));

  dht.begin();
}


void loop() {
  // Wait a few seconds between measurements.
  delay(1000);

  int h = dht.readHumidity();
  prot[0] = h;
  if (isnan(h))
  {
    prot[0] = 0;
  }
  
  float t = dht.readTemperature();
  int tFormat = (t * 10)/2;
  prot[1] = tFormat;
  if (isnan(t))
  {
    prot[1] = 255;
  }
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  prot[2] = 65;
  prot[3] = 97;

  Serial.write(prot, 4);
  Serial.println();
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("% - "));
  Serial.print(h, HEX);
  Serial.print(F("    Temperature: "));
  Serial.print(t);
  Serial.print(F("°C    "));
  Serial.print(tFormat, HEX);
  Serial.print(" - ");
  Serial.println(tFormat);
}
