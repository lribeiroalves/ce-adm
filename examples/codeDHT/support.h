//BIBLIOTECAS
#include "DHT.h"

//DEFINIÇÕES
#define DHTPIN A1     
#define DHTTYPE DHT11  

//DECLARAÇÕES
DHT dht(DHTPIN, DHTTYPE);
byte prot[4];