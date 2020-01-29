// Arduino Library
#include <Arduino.h>

// Project Headers
#include "Serial.h"
#include "Generator.h"
#include "C2192_Anemometer.h"

// Serial Commands
#define GET_AVERAGE_SPEED     1
#define GET_AVERAGE_VOLTAGE   2
#define CLEAR_BUFFERS         3

// Time Interval to Log Data
#define DATA_INTERVAL 100

// Size of Data Buffers
#define BUFFER_SIZE 16

// Buffer Variables
int index;
float speeds[BUFFER_SIZE];
float voltages[BUFFER_SIZE];

float averageSpeed();
float averageVoltage();
int clearBuffers();

// Time Storage
long last;

void setup()
{
  initSerial();
  initAnemometer();
  initGenerator();

  clearBuffers();
  last = 0;
  index = 0;
}


void loop()
{
  // Log Data each Interval
  if(millis()-last > INTERVAL)
  {
    speeds[index] = anemometer.windspeed();
    voltages[index] = gen.voltage();
    index = index + 1;
    index = index % BUFFER_SIZE;
    last = millis();
  }

  // Check for Command
  if(Serial.available())
  {
    byte data = Serial.read();
    switch(data)
    {
      case GET_AVERAGE_SPEED:
        Serial.println(averageSpeed());
        break;
      case GET_AVERAGE_VOLTAGE:
        Serial.println(averageVoltage());
        break;
      case CLEAR_BUFFERS:
        clearBuffers();
        break;
      default:
        Serial.print("ERROR: ");
        Serial.println(data);
        break;
    }
  }
}

float averageSpeed()
{
  float value = 0;
  for(int n = 0; n < BUFFER_SIZE; n++)
  {
    value += speeds[n];
  }
  return value /= BUFFER_SIZE;
}

float averageVoltage()
{
  float value = 0;
  for(int n = 0; n < BUFFER_SIZE; n++)
  {
    value += voltages[n];
  }
  return value /= BUFFER_SIZE;
}

int clearBuffers()
{
  for(int n = 0; n < BUFFER_SIZE; n++)
  {
    speeds[n] = 0;
    voltages[n] = 0;
  }
  return 0;
}
