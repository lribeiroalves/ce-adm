/*
 * There are three serial ports on the ESP known as U0UXD, U1UXD and U2UXD.
 * 
 * U0UXD is used to communicate with the ESP32 for programming and during reset/boot.
 * U1UXD is unused and can be used for your projects. Some boards use this port for SPI Flash access though
 * U2UXD is unused and can be used for your projects.
 * 
*/
//#include <SoftwareSerial.h>
#include "Wire.h"
#define DS1307_ADDRESS 0x68
byte zero = 0x00;
#define RXD2 2
#define TXD2 4
//SoftwareSerial lora(RXD2, TXD2);

const int size_msg = 30;
byte msg[size_msg];
int segundo = 3;
int minuto = 2;
int hora = 1;
int diasemana = 4;
int dia = 4;
int mes = 5;
int ano  = 6;
int controle = 0;

void setup() {
  Serial.begin(9600);
  Serial2.begin(1200, SERIAL_8N1, RXD2, TXD2);
  Wire.begin();
  //setDateTime(); //Configurar na função setDateTime(). Após configurar RTC, comentar a linha dessa função.
  Serial.println("Iniciando TX");
}


void loop() {
  //printDate();
  enviaMensagem ();
}


void setDateTime(){

  byte segundo =      00;  //0-59
  byte minuto =       00;  //0-59
  byte hora =         19;  //0-23
  byte diasemana =    02;  //1-7
  byte dia =          03;  //1-31
  byte mes =          12; //1-12
  byte ano  =         13; //0-99

  Wire.beginTransmission(DS1307_ADDRESS);
  Wire.write(zero); 

  Wire.write(decToBcd(segundo));
  Wire.write(decToBcd(minuto));
  Wire.write(decToBcd(hora));
  Wire.write(decToBcd(diasemana));
  Wire.write(decToBcd(dia));
  Wire.write(decToBcd(mes));
  Wire.write(decToBcd(ano));

  Wire.write(zero); 

  Wire.endTransmission();

}

byte decToBcd(byte val){
// Conversão de decimal para binário
  return ( (val/10*16) + (val%10) );
}

byte bcdToDec(byte val)  {
// Conversão de binário para decimal
  return ( (val/16*10) + (val%16) );
}

void printDate(){

  Wire.beginTransmission(DS1307_ADDRESS);
  Wire.write(zero);
  Wire.endTransmission();

  Wire.requestFrom(DS1307_ADDRESS, 7);

  int segundo = bcdToDec(Wire.read());
  int minuto = bcdToDec(Wire.read());
  int hora = bcdToDec(Wire.read() & 0b111111);    //Formato 24 horas
  int diasemana = bcdToDec(Wire.read());             //0-6 -> Domingo - Sábado
  int dia = bcdToDec(Wire.read());
  int mes = bcdToDec(Wire.read());
  int ano = bcdToDec(Wire.read());

//Exibe a data e hora. Ex.:   3/12/13 19:00:00
  
  Serial.print(dia);
  Serial.print("/");
  Serial.print(mes);
  Serial.print("/");
  Serial.print(ano);
  Serial.print(" ");
  Serial.print(hora);
  Serial.print(":");
  Serial.print(minuto);
  Serial.print(":");
  Serial.println(segundo);

}


void enviaMensagem(){
  msg[0] = controle; //Controle
  msg[1] = (size_msg); //Tamanho mensagem
  msg[2] = hora;
  msg[3] = minuto;
  msg[4] = segundo;
  msg[5] = dia;
  msg[6] = mes;
  msg[7] = ano;
  for (int i = 8; i < 30; i++){
    msg[i] = i-1;
  }
  //msg[8] = 236;

  if(controle < 255){
    controle = controle + 1;
  }
  else{
    controle = 0;
  }
  Serial2.write(msg, 30);

  Serial.println("Send");

  delay(5000);
}