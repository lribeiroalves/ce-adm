#ifndef GYRO_LIB
#define GYRO_LIB

#include "Wire.h"

class GYRO {

private:
  short int gx, gy, gz;
  const int MPU = 0x68;

public:
  // Método construtor, inicializa a comunicação com MPU enviando o comando de acordar
  GYRO() {
    Wire.begin();
    Wire.beginTransmission(MPU);
    Wire.write(0x6B); // endereço de memória do gerenciador de energia
    Wire.write(0);    // comando para acordar e sair do modo padrão de economia de energia
    Wire.endTransmission(true);
  }

  // leitura dos eixos
  byte* read_gyro() {
    static byte* leitura[3] = {0,0,0};

    Wire.beginTransmission(MPU);
    Wire.write(0x43); // primeiro endereço de memória com os dados do giroscópio
    Wire.endTransmission(false);  // encerra a comunicação mas mantém o canal aberto com o MPU
    Wire.requestFrom(MPU, 6, true); // requisita 6 bytes a partir do endereço fornecido (0x43) e encerra o canal com o MPU

    // realiza duas leituras para cada eixo e aloca os 2 bytes em um int de 16bits
    gx = Wire.read() << 8 | Wire.read();
    gy = Wire.read() << 8 | Wire.read();
    gz = Wire.read() << 8 | Wire.read();

    // tratar e armazenar os valores em um array
    leitura[0] = (byte) (max(0, (abs(gx) - 150)) >> 7);
    leitura[1] = (byte) (max(0, (abs(gy) - 150)) >> 7);
    leitura[2] = (byte) (max(0, (abs(gz) - 150)) >> 7);

    return leitura;
  }
};

#endif