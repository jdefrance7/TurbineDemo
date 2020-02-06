// Arduino Library
#include <Arduino.h>

// Project Headers
#include "Serial.h"
#include "Generator.h"
#include "LCDShield.h"
#include "C2192_Anemometer.h"

// Built-In LED Pin for Arduino UNO
#define LED_PIN 13

// Time Interval to Log Data to Internal Buffers (ms)
#define DATA_INTERVAL 100

// Time Interval to Update LCD Display of Averages (ms)
#define DISPLAY_INTERVAL 1000

// Time Interval to Print Averages to Serial Port (ms)
#define PRINT_INTERVAL 500

// Size of Data Buffers
#define BUFFER_SIZE 16

// Buffer Variables
int speedIndex = 0;
int voltageIndex = 0;
float speeds[BUFFER_SIZE];
float voltages[BUFFER_SIZE];

// // Print Variable
// bool BROADCAST = false;

bool LED_STATE = false;

// Setup Function Declarations
int initModules();

// Loop Function Declarations
int logData();
// int checkSerial();
int printData();
int updateDisplay();

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

/*
  checkSerial();

  if(BROADCAST)
  {
      printData();
  }
*/

  printData();

  updateDisplay();
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
    speeds[speedIndex] = anemometer.windspeed();

    // Record Voltage
    voltages[voltageIndex] = gen.voltage();

    // Increment Indexes
    speedIndex = speedIndex + 1;
    speedIndex = speedIndex % BUFFER_SIZE;

    voltageIndex = voltageIndex + 1;
    voltageIndex = voltageIndex % BUFFER_SIZE;

    // Update Data Time
    dataTime = millis();
  }

  return 0;
}

/*
int checkSerial()
{
  char input;

  if(Serial)
  {
    if(Serial.available())
    {
      // Read Byte/Char from Serial
      input = Serial.read();

      // Enter Broadcast Mode
      if(input == 'B')
      {
        BROADCAST = true;
      }

      // Exit Broadcast Mode
      else if(input == 'S')
      {
        BROADCAST = false;
      }

      // Print Single Data Pair to Serial
      else if(input == 'D')
      {
        Serial.print(averageSpeed());
        Serial.print(", ");
        Serial.print(averageVoltage());
        Serial.print("\n");
      }

      // Clear Serial Iput Buffer
      while(Serial.available())
      {
        Serial.read();
      }
    }
    return 0;
  }
  // Error with Serial
  return -1;
}
*/

int printData()
{
  static long printTime = millis();

  if(millis() - printTime > PRINT_INTERVAL)
  { 
    // Print Updated Averages
    Serial.print(averageSpeed());
    Serial.print(", ");
    Serial.print(averageVoltage());
    Serial.print("\n");

    // Update Print Time
    printTime = millis();
  }
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
