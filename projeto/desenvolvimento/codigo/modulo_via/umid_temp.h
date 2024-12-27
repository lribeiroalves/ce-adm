#ifndef UMID_TEMP_LIB
#define UMID_TEMP_LIB

#include "Arduino.h"
#include "DHT.h"

class UMTE {
  
private:
  int dht_pin;
  DHT dht;
  int readings_time; // ms
  unsigned long prev_time = 0;
  byte reading[2] = {0,0};
  bool update_enable = true;

public:
  // método construtor, usando initialization list para instanciar um objeto da classe DHT
  UMTE(int pin, int time)
    : dht_pin(pin), dht(DHT(dht_pin, 11))
  {
    readings_time = time;
    dht.begin();
  }

  // métodos para leituras das informações
  byte temp() {
    float t = dht.readTemperature();

    if (isnan(t)) {
      return 254;
    }
    else {
      return (byte) (t * 5);
    }
  }

  byte umid() {
    float h = dht.readHumidity();
    
    if (isnan(h)) {
      return 254;
    }
    else {
      return (byte) h;
    }
  }

  // ATUALIZAR O UPDATE PARA O PADRÃO DO GIROSCOPIO

  // realiza a leitura caso o período de tempo determinado em readings_time (ms) tenha passado
  void update() {
    unsigned long curr_time = millis(); // verifica o tempo atual

    if (curr_time >= prev_time + readings_time) {
      prev_time = curr_time;

      if (update_enable) {
        reading[0] = temp();
        reading[1] = umid();

        update_enable = false;
      }
    }
  }

  // setter para o update enable
  void enableUpdate() {
    update_enable = true;

    for (int i = 0; i < 2; i++) {
      reading[i] = 0;
    }
  }

  // getters para as leituras
  bool getEnable() const {
    return update_enable;
  }

  byte* getReadings() const {
    static byte _r[2] = {0,0};

    _r[0] = reading[0];
    _r[1] = reading[1];

    return _r;
  }
};

#endif