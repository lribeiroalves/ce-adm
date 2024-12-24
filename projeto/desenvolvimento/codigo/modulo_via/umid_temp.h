#ifndef UMID_TEMP_LIB
#define UMID_TEMP_LIB

#include "Arduino.h"
#include "DHT.h"

class UMTE {
  
private:
  int dht_pin;
  int sensor_type;
  DHT dht;
  int readings_time; // ms
  unsigned long prev_time = 0;

public:
  // método construtor, usando initialization list para instanciar um objeto da classe DHT
  UMTE(int pin, int sensor, int time)
    : dht_pin(pin), sensor_type(sensor), dht(DHT(dht_pin, sensor_type))
  {
    readings_time = time;
    dht.begin();
  }

  // métodos para leituras das informações
  int8_t temp() {
    float t = dht.readTemperature();

    if (isnan(t)) {
      return 254;
    }
    else {
      return (int8_t) (t * 5);
    }
  }

  int8_t umid() {
    float h = dht.readHumidity();
    
    if (isnan(h)) {
      return 254;
    }
    else {
      return (int8_t) h;
    }
  }

  // realiza a leitura caso o período de tempo determinado em readings_time (ms) tenha passado
  int8_t* update() {
    int8_t readings[2] = {256, 256};

    unsigned long curr_time = millis(); // verifica o tempo atual

    if (curr_time >= prev_time + readings_time) {
      readings[0] = temp();
      readings[1] = umid();
    }

    return readings;
  }
};

#endif