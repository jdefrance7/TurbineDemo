#include "C2192_Anemometer.h"

C2192_Anemometer anemometer = C2192_Anemometer(ANEMOMETER_PIN);

C2192_Anemometer::C2192_Anemometer(int pin)
{
  _pin = pin;
}

int C2192_Anemometer::init()
{
  // Check Valid Pin Assignment
  if(_pin < 0)
  {
    return -1;
  }

  // Set Pin to Input
  pinMode(_pin, INPUT);

  // Return Success
  return 0;
}

float C2192_Anemometer::windspeed()
{
  // Check Valid Pin Assignment
  if(_pin < 0)
  {
    return -1;
  }

  // Read Digital Voltage Value
  float voltage = analogRead(_pin);

  // Convert to Analog Float Voltage
  voltage *= 5;
  voltage /= 1024;

  // Convert Voltage to Windspeed (see datasheet)
  return ((20*voltage) - 7.6);
}

int initAnemometer()
{
  return anemometer.init();
}
