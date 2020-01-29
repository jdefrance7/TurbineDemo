#include "Generator.h"

Generator gen = Generator(GENERATOR_PIN);

Generator::Generator(int pin)
{
  _pin = pin;
}

int Generator::init()
{
  if(_pin < 0)
  {
    return -1;
  }

  pinMode(_pin, INPUT);

  return 0;
}

float Generator::voltage()
{
  return 5.0*analogRead(pin)/1024;
}

int initGenerator()
{
  return gen.init();
}
