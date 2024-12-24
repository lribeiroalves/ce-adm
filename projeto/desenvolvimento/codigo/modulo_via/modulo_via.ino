#include "umid_temp.h"    // leitura dados do sensor de umidade e temperatura
// #include "gyro.h"         // leitura de dados do giroscopio
// #include "clock.h"        // controle do RTC
// #include "salva_dados.h"  // salvamento local dos dados adquiridos

// PINAGEM
#define DHT_PIN 33

UMTE dht = UMTE(33, 11, 1000);

void setup() {
  Serial.begin(9600);
}

void loop() {
  int8_t* leitura = dht.update();

  // Serial.println(leitura[1]);

  delay(1000);

  // if ((leitura[0] != 0) || (leitura[1] != 0)) {
  //   Serial.print("Temperatura: ");
  //   Serial.print(leitura[0] / 5);
  //   Serial.println(" C");
  //   Serial.print("Umidade: ");
  //   Serial.print(leitura[1]);
  //   Serial.println("%");
  // }
}
