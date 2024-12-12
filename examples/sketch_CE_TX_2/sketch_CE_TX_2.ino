//BIBLIOTECAS
#include "DHT.h"
#include <ESP32Time.h>

//DEFINIÇÕES
#define DHTPIN 27     
#define DHTTYPE DHT11  

//DECLARAÇÕES
DHT dht(DHTPIN, DHTTYPE);
ESP32Time rtc;
byte prot[11];


void setup() {
  Serial.begin(9600);
  Serial2.begin(1200, SERIAL_8N1, 2, 4);
  //Serial.println(F("DHTxx test!"));

  //DHT pins config
  pinMode(26, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(26, HIGH);
  digitalWrite(12, LOW);

  dht.begin();
  rtc.setTime(0, 45, 15, 9, 12, 2024);
}


void loop() {
  // Wait a few seconds between measurements.
  delay(1000);

   int h = dht.readHumidity();
   prot[6] = h;
  if (isnan(h))
  {
    prot[6] = 0;
  }
  
  float t = dht.readTemperature();
  int tFormat = (t * 10)/2;
  prot[7] = tFormat;
  if (isnan(t))
  {
    prot[7] = 255;
  }
  
  // Check if any reads failed and exit early (to try again).
  /*if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }*/

	prot[5] = rtc.getSecond();
	prot[4] = rtc.getMinute();
	prot[3] = rtc.getHour(true);
	prot[0] = rtc.getDay();
	prot[1] = rtc.getMonth();
	prot[2] = rtc.getYear() - 2000;

  Serial.write(prot, 11);
  Serial2.write(prt, 11);
  Serial.print(",");
  /*Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("% - "));
  Serial.print(h, HEX);
  Serial.print(F("    Temperature: "));
  Serial.print(t);
  Serial.print(F("°C    "));
  Serial.print(tFormat, HEX);
  Serial.print(" - ");
  Serial.println(tFormat);*/
}
