#ifndef dht_lib
#define dht_lib

#include "Arduino.h"
#include "DHT.h"

class MyDHT {
private:
  int dhtPin;
  int sensorType;
  DHT dht;

public:
  MyDHT(int pin, int sensor)
    : dhtPin(pin), sensorType(sensor), dht(DHT(dhtPin, sensorType))
  {
    dht.begin();
  }

  float temp() {
    float t = dht.readTemperature();
    return t;
  }
  
};

#endif