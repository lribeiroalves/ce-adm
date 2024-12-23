//BIBLIOTECAS
#include "DHT.h"

//DEFINIÇÕES
#define DHTPIN 2     
#define DHTTYPE DHT11  

//DECLARAÇÕES
DHT dht(DHTPIN, DHTTYPE);
byte prot[4];