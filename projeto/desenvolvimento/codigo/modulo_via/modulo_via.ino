#include "umid_temp.h"    // leitura dados do sensor de umidade e temperatura
#include "gyro.h"         // leitura de dados do giroscopio
// #include "clock.h"        // controle do RTC
// #include "salva_dados.h"  // salvamento local dos dados adquiridos
#include "Wire.h"

// PINAGEM
#define DHT_PIN 33
#define GIRO_SCL 22
#define GIRO_SDA 21
#define SD_MISO 19
#define SD_MOSI 23
#define SD_SCK 18
#define SD_CS 5
#define LORA_RX 26
#define LORA_TX 27

// INSTANCIAS
UMTE dht = UMTE(DHT_PIN, 1000);
GYRO gyro = GYRO();

// VARIAVEIS GLOBAIS

void setup() {
  Serial.begin(115200);
  gyro.begin();
}

// criar uma classe LORA que contenha o método update, que a cada segundo coleta os valores de cada sensor e envia pelo rádio

void loop() {
  byte* leitura = gyro.read_gyro();

  for (int i = 0; i < 3; i++) {
    Serial.print(leitura[i]);
    Serial.print(" ");
  }

  Serial.println();

  delay(500);
}
