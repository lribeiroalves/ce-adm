#include <Arduino.h>

class LED {
  int ledPin;

  public:
  LED(int pin) {
    ledPin = pin;
    pinMode(ledPin, OUTPUT);
  }

  void acender() {
    digitalWrite(ledPin, HIGH);
  }

  void apagar() {
    digitalWrite(ledPin, LOW);
  }
};