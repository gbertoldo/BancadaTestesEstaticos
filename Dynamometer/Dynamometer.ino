#include "HX711.h"
#include <EEPROM.h>


uint8_t pinData  = A4;
uint8_t pinClock = A5;

HX711 loadcell;

float conversionFactor = 1.0;

void setup()
{
  Serial.begin(115200);

  loadcell.begin(pinData, pinClock);

  loadcell.tare();

  EEPROM.get(0,conversionFactor);

  loadcell.set_scale(conversionFactor);
}


void loop()
{
  
  if ( Serial.available() > 0 )
  {
    char cmd = Serial.read();

    if ( cmd == 's' )
    {
      conversionFactor = Serial.parseFloat();
      loadcell.set_scale(conversionFactor);
      EEPROM.put(0,conversionFactor);
    }
    if ( cmd == 'g' )
    {
      Serial.print("<");
      Serial.print("2,");
      Serial.print(loadcell.get_scale(),5);
      Serial.println(">");
    }
  }
  
  float  time = millis()*1E-3;
  float force = loadcell.get_units();
  
  Serial.print("<");
  Serial.print("1,");
  Serial.print(time,3);
  Serial.print(",");
  Serial.print(force,4);
  Serial.println(">");
  
}
