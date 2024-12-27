#ifndef CLOCK_LIB
#define CLOCK_LIB

#include <Arduino.h>
#include <ESP32Time.h>

class CLOCK {

private:
  ESP32Time rtc;

public:
  //método construtor que inicializa o rtc e seta o horário inicial
  CLOCK(int sec, int min, int hor, int dia, int mes, int ano, int ms=0) {
    rtc.setTime(sec, min, hor, dia, mes, ano, ms);
  }

  byte* getTime() {
    static byte _t[6] = {0,0,0,0,0,0};

    _t[0] = rtc.getDay();
    _t[1] = rtc.getMonth();
    _t[2] = rtc.getYear() - 2000;
    _t[3] = rtc.getHour(true);
    _t[4] = rtc.getMinute();
    _t[5] = rtc.getSecond();

    return _t;
  }
};

#endif