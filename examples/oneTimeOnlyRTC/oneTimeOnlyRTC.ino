//https://www.robocore.net/tutoriais/primeiros-passos-rtc-ds1307-com-arduino?srsltid=AfmBOorAc9X_yI7iZ0_KTN5-u2hGvDI56mQILw-3UH-vVOaAypcVIxxW
// Date and time functions using a DS1307 RTC connected via I2C and Wire lib
#include "RTClib.h"

RTC_DS1307 rtc;

int time_set [6] = {2024, 11, 26, 5, 35, 0};

void setup () {
  Serial.begin(9600);

  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  rtc.adjust(DateTime(time_set[0], time_set[1], time_set[2], time_set[3], time_set[4], time_set[5]));
}

void loop () {
    
    DateTime now = rtc.now();

    int protocol_h = ((now.year() - time_set[0]) + (now.month() - time_set[1]) + (now.day() - time_set[2]));
    int protocol_l = ((now.hour() - time_set[3]) + (now.minute() - time_set[4]) + (now.second() - time_set[5]));

    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    //Serial.print(" (");
    //Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
    Serial.print("   ");
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.println();

    Serial.println(protocol_h);
    Serial.println(protocol_l);

    Serial.print("Year now -> ");
    Serial.print(now.year(), DEC);
    Serial.print("    Year set -> ");
    Serial.println(time_set[0], DEC);
    Serial.print("Month now -> ");
    Serial.print(now.month());
    Serial.print("    Month set -> ");
    Serial.println(time_set[1]);
    Serial.print("Day now -> ");
    Serial.print(now.day());
    Serial.print("    Day set -> ");
    Serial.println(time_set[2]);
    Serial.println();
    Serial.println();
    delay(1000);
}
