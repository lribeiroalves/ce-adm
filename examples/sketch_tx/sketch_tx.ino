//BIBLIOTECAS
#include "DHT.h"
#include <ESP32Time.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

//DEFINIÇÕES
#define DHTPIN 27     
#define DHTTYPE DHT11  
#define BUILT_LED 2

//DECLARAÇÕES
DHT dht(DHTPIN, DHTTYPE);
ESP32Time rtc;
const int MPU=0x68;
short GyX,GyY,GyZ;
byte protocol[12];
bool LED;
File myFile;
const int cs = 5;

void WriteData(const char * path, const char * data) {
  myFile = SD.open(path, FILE_APPEND);

  if (myFile) {
    // escrever msg no SD
  }
  else {
    Serial.println("Não foi possível abrir o arquivo");
  }
}

void setup() {
  Serial.begin(9600);
  Serial2.begin(1200, SERIAL_8N1, 32, 33); 

  // Inicialização do Cartão SD
  Serial.println("Inicializando SD Card");
  if (!SD.begin(cs)) {
    Serial.println("Falha na Inicialização do cartão SD");
    return;
  }
  Serial.println("Inicialização do cartão SD concluída.");

  //DHT pins config
  pinMode(26, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(BUILT_LED,OUTPUT);
  digitalWrite(26, HIGH);
  digitalWrite(12, LOW);

  dht.begin();
  rtc.setTime(0, 0, 3, 11, 12, 2024);
  
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
  Wire.write(0); 
  Wire.endTransmission(true);
}


void loop() {

  short iteracao[3] = {0, 0, 0};
  for (int8_t i = 0; i < 9; i++)
  {
    Wire.beginTransmission(MPU);
    Wire.write(0x43);  // starting with register 0x43 (GYRO_XOUT_H)
    Wire.endTransmission(false);
    //Solicita os dados do sensor
    Wire.requestFrom(MPU,6,true);  

    GyX=Wire.read()<<8|Wire.read();  //0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    if (GyX < 0) {GyX = GyX * (- 1);}
    GyX = GyX - 150;
    if (GyX < 0) {GyX = 0;}
    if (GyX > iteracao[0]) {iteracao[0] = GyX;}                  
  
    GyY=Wire.read()<<8|Wire.read();  //0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    if (GyY < 0) {GyY = GyY * (- 1);}
    GyY = GyY - 150;
    if (GyY < 0) {GyY = 0;}
    if (GyY > iteracao[1]) {iteracao[1] = GyY;}

    GyZ=Wire.read()<<8|Wire.read();  //0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    if (GyZ < 0) {GyZ = GyZ * (- 1);}
    GyZ = GyZ - 150;
    if (GyZ < 0) {GyZ = 0;}
    if (GyZ > iteracao[2]) {iteracao[2] = GyZ;}

    delay(100);
  }

  protocol[9] = iteracao[0] / 128;
  protocol[10] = iteracao[1] / 128;
  protocol[11] = iteracao[2] / 128;

  //UMIDADE
  int8_t h = dht.readHumidity();
  protocol[6] = h;
  if (isnan(h))
  {
    protocol[7] = 254;
  }
  
  float t = dht.readTemperature();
  int8_t tFormat = (t * 10)/2;
  protocol[7] = tFormat;
  if (isnan(t))
  {
    protocol[8] = 254;
  }
  
  //RTC
  protocol[1] = rtc.getDay();
	protocol[2] = rtc.getMonth();
	protocol[3] = rtc.getYear() - 2000;
	protocol[4] = rtc.getHour(true);
  protocol[5] = rtc.getMinute();
	protocol[6] = rtc.getSecond();

  protocol[0] = ","; //enviando a vírgula dentro do pacote

  //ESCRITA
  // Serial2.write(",");
  Serial2.write(protocol, 12);
  // Serial.print(",");
  Serial.write(protocol, 12);
  Serial.println();
  
  //  PARA VISUALIZAÇÃO DOS ARQUIVOS NO PROMPT
  for(__int8_t i = 0; i < 12; i++)
  {
    Serial.print(protocol[i], HEX);
    Serial.print("  ");
  }
  Serial.println();
  
  LED = !LED;
  digitalWrite(BUILT_LED,LED);

  delay(100);
}
