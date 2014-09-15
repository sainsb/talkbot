
#include "SPI.h"
#include "Adafruit_WS2801.h"

uint8_t dataPin  = 15;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 14;    // Green wire on Adafruit Pixels

// Don't forget to connect the ground wire to Arduino ground,
// and the +5V wire to a +5V supply

// Set the first variable to the NUMBER of pixels in a row and
// the second value to number of pixels in a column.
Adafruit_WS2801 strip = Adafruit_WS2801((uint16_t)15, (uint16_t)1, dataPin, clockPin);

void setup(){
 strip.begin();
 // Update LED contents, to start they are all 'off'
 strip.show();
 //Serial2.begin(9600);
 Serial3.begin(9600);
}
 
void loop(){
  
   while (Serial3.available() > 0) {
     
    int who = Serial3.parseInt(); 
    // look for the next valid integer in the incoming serial stream:
    int red = Serial3.parseInt(); 
    // do it again:
    int green = Serial3.parseInt(); 
    // do it again:
    int blue = Serial3.parseInt(); 

    // look for the newline. That's the end of your
    // sentence:
    if (Serial3.read() == '\n') {
      // constrain the values to 0 - 255 and invert
      // if you're using a common-cathode LED, just use "constrain(color, 0, 255);"
      red = constrain(red, 0, 255);
      green = constrain(green, 0, 255);
      blue = constrain(blue, 0, 255);
      
      strip.setPixelColor(who, 0, red, green, blue);
    
      strip.show();
      /* debug
      Serial2.write( 0xFE );
      Serial2.write( 0x01 );
      delay(10);
      Serial2.write( 0xFE );
      Serial2.write( 128 );
      delay(10);
      Serial2.print(who, DEC);
      Serial2.print(' ');
      Serial2.print(red, DEC);
      Serial2.print(' ');
      Serial2.print(green, DEC);
      Serial2.print(' ');      
      Serial2.print(blue, DEC);
      */
    }
  }
}