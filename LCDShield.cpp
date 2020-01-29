#include "LCDShield.h"

Adafruit_RGBLCDShield lcd = Adafruit_RGBLCDShield();

int initLCD()
{
  // Initialize LCD with Width & Height
  lcd.begin(LCD_CHAR_WIDTH, LCD_CHAR_HEIGHT);

  // Turn on Backlight
  lcd.setBacklight(0x7);

  // Return Success
  return 0;
}
