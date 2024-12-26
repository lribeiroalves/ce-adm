#ifndef GYRO_LIB
#define GYRO_LIB

#include "Arduino.h"
#include "Wire.h"

class GYRO {

private:
  short int gx, gy, gz;
  const int MPU = 0x68;
  bool begin_control = false;
  long reading_time;
  unsigned long prev_time = 0;
  byte reading[4] = {0,0,0,0}; // variável que armazenará as leituras
  bool update_enable = true; // variável que permite ou não novas leituras pelo método update

public:
  // Método construtor, inicializa a comunicação com MPU enviando o comando de acordar
  GYRO(long time) {
    reading_time = time;
  }

  //Initialization
  void begin() {
    if (!begin_control) {
      Wire.begin();
      Wire.beginTransmission(MPU);
      Wire.write(0x6B); // endereço de memória do gerenciador de energia
      Wire.write(0);    // comando para acordar e sair do modo padrão de economia de energia
      Wire.endTransmission(true);
      begin_control = true;
    }
  }

  // leitura dos eixos
  byte* read_gyro() {
    static byte leitura[3] = {0,0,0};

    Wire.beginTransmission(MPU);
    Wire.write(0x43); // primeiro endereço de memória com os dados do giroscópio
    Wire.endTransmission(false);  // encerra a comunicação mas mantém o canal aberto com o MPU
    Wire.requestFrom(MPU, 6, true); // requisita 6 bytes a partir do endereço fornecido (0x43) e encerra o canal com o MPU

    // realiza duas leituras para cada eixo e aloca os 2 bytes em um int de 16bits
    gx = Wire.read() << 8 | Wire.read();
    gy = Wire.read() << 8 | Wire.read();
    gz = Wire.read() << 8 | Wire.read();

    // tratar e armazenar os valores em um array
    leitura[0] = (byte) (max(0, (abs(gx) - 0)) >> 7);
    leitura[1] = (byte) (max(0, (abs(gy) - 0)) >> 7);
    leitura[2] = (byte) (max(0, (abs(gz) - 0)) >> 7);

    return leitura;
  }  

  void update() {
    unsigned long curr_time = millis();
    
    if (curr_time >= prev_time + reading_time) {
      prev_time = curr_time;
      
      // verifica se a leitura está habilitada
      if (update_enable) {
        byte* r = read_gyro();

        reading[0] = max(reading[0], r[0]);
        reading[1] = max(reading[1], r[1]);
        reading[2] = max(reading[2], r[2]);

        reading[3]++;

        // apos 10 leituras, o update é desabilitado até que os dados sejam enviados pelo Lora
        if (reading[3] == 10) {
          update_enable = false;
        }
      }
    }
  }

  // setter para o update enable
  void enableUpdate() {
    update_enable = true;

    for (int i = 0; i < 4; i++) {
      reading[i] = 0;
    }
  }

  // getters para as leituras
  bool getEnable() const {
    return update_enable;
  }

  byte* getReadings() const {
    static byte _r[3] = {0,0,0};

    _r[0] = reading[0];
    _r[1] = reading[1];
    _r[2] = reading[2];

    return _r;
  }

};

#endif