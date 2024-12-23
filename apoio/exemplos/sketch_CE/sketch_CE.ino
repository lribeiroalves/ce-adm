//INCLUSÃO DE BIBLIOTECAS
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

/*DEFINIÇÃO DE PINOS DO ARDUINO. LEMBRE-SE: O PINO ONDE VOCÊ CONECTOU O TX SERÁ O RX AQUI NO CÓDIGO E VICE-VERSA. ISSO É POR CAUSA DA
COMUNICAÇÃO SERIAL. PARA MAIS DETALHES, VOCÊ PODE CONSULTAR NOSSO BLOG*/
int RXPin = 2;
int TXPin = 3;

int GPSBaud = 9600;

//CRIANDO UM O BJETO PARA COMUNICAR COM A BIBLIOTECA
TinyGPSPlus gps;

// CRIANDO UMA PORTA SERIAL gpsSerial PARA CONVERSAR COM MÓDULO
SoftwareSerial gpsSerial(RXPin, TXPin);

void setup()
{
// INICIA A SERIAL
Serial.begin(9600);

// INICIA A PORTA SERIAL DO SOFTWARE NO BAUD PADRÃO DO GPS, COMO DETERMINAMOS ACIMA:9600
gpsSerial.begin(GPSBaud);
}

void loop()
{
// TODA VEZ QUE FOR LIDA UMA NOVA SENTENÇA NMEA, CHAMAREMOS A FUNÇÃO displayInfo() PARA MOSTRAR OS DADOS NA TELA
while (gpsSerial.available() > 0)
if (gps.encode(gpsSerial.read()))
displayInfo();

//SE EM 5 SEGUNDOS NÃO FOR DETECTADA NENHUMA NOVA LEITURA PELO MÓDULO,SERÁ MOSTRADO ESTA MENSGEM DE ERRO.
if (millis() > 5000 && gps.charsProcessed() < 10)
{
Serial.println("Sinal GPS não detectado");
while(true);
}
}

void displayInfo()//FUNÇÃO RESPONSAVEL PELA LEITURA DOS DADOS
{
if (gps.location.isValid())//SE A LOCALIZAÇÃO DO SINAL ENCONTRADO É VÁLIDA, ENTÃO
{
Serial.print("Latitude: ");
Serial.println(gps.location.lat(), 6);//IMPRIME NA SERIAL O VALOR DA LATIDUE LIDA
Serial.print("Longitude: ");
Serial.println(gps.location.lng(), 6);//IMPRIME NA SERIAL O VALOR DA LONGITUDE LIDA

}
else
{
Serial.println("Não detectamos a localização");//SE NÃO HOUVER NENHUMA LEITURA, IMPRIME A MENSAGEM DE ERRO NA SERIAL
}

Serial.print("Data: ");
if (gps.date.isValid())//IMPRIME A DATA NA SERIAL
{
Serial.print(gps.date.day());//LEITURA DO DIA
Serial.print("/");
Serial.print(gps.date.month());//LEITURA DO MêS
Serial.print("/");
Serial.println(gps.date.year());//LEITURA DO ANO
}
else
{
Serial.println("Erro");//SE NÃO HOUVER NENHUMA LEITURA, IMPRIME A MENSAGEM DE ERRO NA SERIAL
}

Serial.print("Time: "); //LEITURA DA HORA PARA SER IMPRESSA NA SERIAL
if (gps.time.isValid())
{
if (gps.time.hour() < 10) Serial.print(F("0"));
Serial.print(gps.time.hour() - 3); //AJUSTA O FUSO HORARIO PARA NOSSA REGIAO (FUSO DE SP 03:00, POR ISSO O -3 NO CÓDIGO) E IMPRIME NA SERIAL
Serial.print(":");
if (gps.time.minute() < 10) Serial.print(F("0"));
Serial.print(gps.time.minute());//IMPRIME A INFORMAÇÃO DOS MINUTOS NA SERIAL
Serial.print(":");
if (gps.time.second() < 10) Serial.print(F("0"));
Serial.print(gps.time.second());//IMPRIME A INFORMAÇÃO DOS SEGUNDOS NA SERIAL
}
else
{
Serial.println("Não detectamos o horário atual");//SE NÃO HOUVER NENHUMA LEITURA, IMPRIME A MENSAGEM DE ERRO NA SERIAL
}

Serial.println();
Serial.println();
delay(1000);
}