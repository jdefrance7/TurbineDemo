// Arduino Library
#include <Arduino.h>

// Project Headers
#include "Serial.h"
#include "Generator.h"
#include "LCDShield.h"
#include "C2192_Anemometer.h"

// Built-In LED Pin for Adafruit M0
#define LED_PIN 13

// Serial Commands
#define GET_AVERAGE_SPEED     1
#define GET_AVERAGE_VOLTAGE   2
#define CLEAR_BUFFERS         3
#define GET_SPEED_BUFFER      4
#define GET_VOLTAGE_BUFFER    5

// Time Interval to Log Data (ms)
#define DATA_INTERVAL 100

// Time Interval to Update Display (ms)
#define DISPLAY_INTERVAL 1000

// Size of Data Buffers
#define BUFFER_SIZE 16

// Buffer Variables
int index;
float speeds[BUFFER_SIZE];
float voltages[BUFFER_SIZE];

// Setup Function Declarations
int initModules();

// Loop Function Declarations
int logData();
int updateDisplay();
int handleCommand();

// Support Function Declarations
int toggleLED();
float averageSpeed();
float averageVoltage();
int clearBuffers();

void setup()
{
  initModules();

  clearBuffers();
}

void loop()
{
  logData();

  updateDisplay();

  handleCommand();
}

int initModules()
{
  pinMode(LED_PIN, OUTPUT);

  if(initSerial())
  {
    toggleLED();
  }

  if(initAnemometer())
  {
    toggleLED();
  }

  if(initGenerator())
  {
    toggleLED();
  }

  if(initLCD())
  {
    toggleLED();
  }

  return 0;
}

int toggleLED()
{
  while(1)
  {
    digitalWrite(LED_PIN, HIGH);
    delay(300);
    digitalWrite(LED_PIN, LOW);
    delay(300);
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

int logData()
{
  // Static Variable for Recording Data
  static long dataTime = millis();

  // Get Data each Data Interval
  if(millis()-dataTime > DATA_INTERVAL)
  {
    // Record Windspeed
    speeds[index] = anemometer.windspeed();

    // Record Voltage
    voltages[index] = gen.voltage();

    // Increment Index
    index = index + 1;
    index = index % BUFFER_SIZE;

    // Update Data Time
    dataTime = millis();
  }

  return 0;
}

int updateDisplay()
{
  // Static Variable for Updating Display
  static long displayTime = millis();

  // Update Display each Display Interval
  if(millis() - displayTime > DISPLAY_INTERVAL)
  {
    // Clear Display
    lcd.clear();

    // Print Average Windspeed
    lcd.setCursor(0,0);
    lcd.print("WIND: ");
    lcd.print(averageSpeed());
    lcd.print(" m/s");

    // Print Average Voltage
    lcd.setCursor(1,0);
    lcd.print("VOLT: ");
    lcd.print(averageVoltage());
    lcd.print(" V");

    // Update Display Time
    displayTime = millis();
  }

  return 0;
}

int handleCommand()
{
  // Data Variable for Serial Commands
  static byte data;

  // Check Serial Module for Command
  if(Serial.available())
  {
    data = Serial.read();
    switch(data)
    {
      case GET_AVERAGE_SPEED:
        Serial.print("SPEED ");
        Serial.println(averageSpeed());
        break;
      case GET_AVERAGE_VOLTAGE:
        Serial.print("VOLTAGE ");
        Serial.println(averageVoltage());
        break;
      case CLEAR_BUFFERS:
        Serial.println("CLEAR");
        clearBuffers();
        break;
      case GET_SPEED_BUFFER:
        Serial.print("SPEEDS ");
        Serial.println(speeds);
        break;
      case GET_VOLTAGE_BUFFER:
        Serial.print("VOLTAGES ");
        Serial.println(voltages);
      default:
        Serial.print("ERROR ");
        Serial.println(data);
        break;
    }
  }

  return 0;
}
