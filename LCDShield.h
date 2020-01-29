#ifndef LCDSHIELD_H
#define LCDSHIELD_H

// Arduino Library
#include <Arduino.h>

// LCD Library
#include <Adafruit_RGBLCDShield.h>

#define LCD_CHAR_HEIGHT 2
#define LCD_CHAR_WIDTH 16

int initLCD();

extern Adafruit_RGBLCDShield lcd;

#endif // LCDSHIELD_H
