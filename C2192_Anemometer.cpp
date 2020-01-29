#include "C2192_Anemometer.h"

C2192_Anemometer anemometer = Anemometer(ANEMOMETER_PIN);

C2192_Anemometer::Anemometer(int pin)
{
  _pin = pin;
}

int C2192_Anemometer::init()
{
  if(_pin < 0)
  {
    return -1;
  }

  pinMode(_pin, INPUT);

  return 0;
}

float C2192_Anemometer::windspeed()
{
  if(_pin < 0)
  {
    return -1;
  }
  float voltage = analogRead(_pin);
  voltage *= 5;
  voltage /= 1024;
  return ((20*voltage) - 7.6);
}

int initAnemometer()
{
  return anemometer.init();
}
