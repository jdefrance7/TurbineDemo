#ifndef C2192_ANEMOMETER_H
#define C2192_ANEMOMETER_H

#include <Arduino.h>

#define ANEMOMETER_PIN 8

class C2192_Anemometer()
{
public:
  Anemometer(int pin);
  int init();
  float windspeed();
private:
  int _pin;
};

extern C2192_Anemometer anemometer;

int initAnemometer();

#endif // C2192_ANEMOMETER_H
