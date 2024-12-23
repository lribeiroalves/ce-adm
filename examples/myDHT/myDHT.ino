#include "dht_lib.h"

MyDHT dht = MyDHT(23, 11);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  Serial.println(dht.temp());
}
