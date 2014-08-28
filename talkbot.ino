#include "SPI.h"
#include "Adafruit_WS2801.h"

uint8_t dataPin  = 2;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 1;    // Green wire on Adafruit Pixels

// Don't forget to connect the ground wire to Arduino ground,
// and the +5V wire to a +5V supply

// Set the first variable to the NUMBER of pixels in a row and
// the second value to number of pixels in a column.
Adafruit_WS2801 strip = Adafruit_WS2801((uint16_t)25, (uint16_t)1, dataPin, clockPin);

int incomingByte = 0;
void setup() {
    
  strip.begin();
  Serial.begin(9600);
  // Update LED contents, to start they are all 'off'
  strip.show();
}

void loop(){

   while (Serial.available() > 0) {
     
    int who = Serial.parseInt(); 
    // look for the next valid integer in the incoming serial stream:
    int red = Serial.parseInt(); 
    // do it again:
    int green = Serial.parseInt(); 
    // do it again:
    int blue = Serial.parseInt(); 

    // look for the newline. That's the end of your
    // sentence:
    if (Serial.read() == '\n') {
      // constrain the values to 0 - 255 and invert
      // if you're using a common-cathode LED, just use "constrain(color, 0, 255);"
      red = constrain(red, 0, 255);
      green = constrain(green, 0, 255);
      blue = constrain(blue, 0, 255);
      
      strip.setPixelColor(who, 0, red, green, blue);
    
      strip.show();
      // fade the red, green, and blue legs of the LED: 
      //analogWrite(redPin, red);
      //analogWrite(greenPin, green);
      //analogWrite(bluePin, blue);

      // print the three numbers in one string as hexadecimal:
      Serial.print(red, DEC);
      Serial.print(green, DEC);
      Serial.println(blue, DEC);
    }
  }
}

