#include "pisca_led.h"

PiscaLed led1 = PiscaLed(2, 1000, 500);
PiscaLed led2 = PiscaLed(4, 300, 1200);

void setup() {
}

void loop() {
  led1.Update();
  led2.Update();
}
