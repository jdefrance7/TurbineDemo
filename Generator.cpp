#include "Generator.h"

Generator gen = Generator(GENERATOR_PIN);

Generator::Generator(int pin)
{
  _pin = pin;
}

int Generator::init()
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

float Generator::voltage()
{
  // Convert Digital Value to Float Voltage
  return (5.0*analogRead(_pin))/1024;
}

int initGenerator()
{
  return gen.init();
}
