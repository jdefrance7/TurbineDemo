#ifndef GENERATOR_H
#define GENERATOR_H

// Arduino Library
#include <Arduino.h>

#define GENERATOR_PIN 7

class Generator
{
public:
  Generator(int pin);
  float voltage();
  int init();
private:
  int _pin;
};

extern Generator gen;

int initGenerator();

#endif // GENERATOR_H
