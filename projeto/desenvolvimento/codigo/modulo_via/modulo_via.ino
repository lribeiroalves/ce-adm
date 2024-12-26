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
GYRO gyro = GYRO(80);

// VARIAVEIS GLOBAIS
int c = 0;
long p_time = 0;
long c_time = 0;
long tempo = 0;

void setup() {
  delay(3000);
  Serial.begin(115200);
  gyro.begin();
  delay(5000);
  p_time = millis();
}

// criar uma classe LORA que contenha o método update, que a cada segundo coleta os valores de cada sensor e envia pelo rádio

void loop() {
  gyro.update();

  if (!gyro.getEnable()) {
    c_time = millis();
    tempo = c_time - p_time;
    p_time = c_time;

    byte* l = gyro.getReadings();
    for (int i = 0; i < 3; i++) {
      Serial.print(l[i]);
      Serial.print(" ");
    }

    Serial.println();
    Serial.print("tempo: ");
    Serial.print(tempo);
    Serial.println("ms");

    gyro.enableUpdate();
  }

  // Serial.println(gyro.getEnable());


  //   for (int i = 0; i < 3; i++) {
  //     Serial.print(l[i]);
  //     Serial.print(" ");
  //   }

  // gyro.update();

  // Serial.println();

  // delay(1000);

  // c++;

  // if (c >= 20) {
  //   gyro.enableUpdate();
  //   c = 0;
  // }
}
