// vim: ts=4 sw=4 ft=cpp ai cindent

/**
 * Strobe Alert Embedded Software
 *
 * FB Hackathon
 * January 2015
 * Author: Jason McHugh  mchughj@fb.com
 *
 * If you have questions about this then feel free to ask.
 *
 * This is the application that runs on an Atmel processor, listens
 * for commands from the serial and uses a MOSFET (the RFP30N06LE)
 * to switch on and off a strobe light.
 */

#include <Serial>

#define CONTROL_PIN 2
#define BUTTON_PIN 4

#define BUTTON_TIME_DEBOUNCE 50
#define BUTTON_PRESS_ALARM_TIME 5000

int32_t durationRemaining;
unsigned long lastTimeSeen; 
unsigned long buttonPressTime;
int buttonState;

void setup() {
    Serial.begin(9600);
    delay(500);
    
    pinMode( CONTROL_PIN, OUTPUT );
    pinMode( BUTTON_PIN, INPUT_PULLUP );

    Serial.println( F("Done with setup") );
    durationRemaining = 0;
    buttonPressTime = 0;
    lastTimeSeen = millis();
}

void handleButtonPress() { 
  if( durationRemaining == -1 || durationRemaining > 0 ) { 
    durationRemaining = 0;
  } else {
    durationRemaining += BUTTON_PRESS_ALARM_TIME;
  }
}

void loop() {
    if( Serial.available() > 0 ) {
        consume_next_command();
    }
    
    unsigned long currentTime = millis();

    if( digitalRead( BUTTON_PIN ) == LOW ) {
      // The button is depressed.  Look to see if this is the first notification.
      if( buttonState != 1 ) { 
        // Ensure that a quick on-off-on doesn't trigger the same button action.
        if( currentTime - buttonPressTime > BUTTON_TIME_DEBOUNCE ) {
           Serial.print( F( "Button has been pressed; time: " ));
           Serial.println( currentTime );
           buttonState = 1;
           buttonPressTime = currentTime;
           handleButtonPress();
        }
      }
    } else if( buttonState == 1 ) { 
      Serial.println( F( "Button has been released;" ));
      buttonState = 0;
    }  
   
    unsigned long millisPassed = currentTime - lastTimeSeen;
    if( durationRemaining > 0 ) { 
      Serial.print( F( "Alarm is active; millisPassed: " ));
      Serial.print(millisPassed);
      Serial.print( F( ", durationRemaining: " ));
      Serial.println( durationRemaining );
      
      durationRemaining -= millisPassed;
      if( durationRemaining < 0 ) { 
        durationRemaining = 0;
       
        Serial.println( F( "Alarm duration has ended;" ));
      }
    }
    lastTimeSeen = currentTime;
    
    if( durationRemaining > 0 || durationRemaining == -1 ) {
      digitalWrite( CONTROL_PIN, 1 );
    } else {
      digitalWrite( CONTROL_PIN, 0 );
    }
    delay(10);
}

// Read the next command and handle consuming that specific command.
void consume_next_command() {
    Serial.println( F("Going to consume next command") );
    uint32_t command = Serial.parseInt();
    Serial.print( F("Command; command: ") );
    Serial.println( command );
    if( command == 1 ) {
        uint32_t duration = Serial.parseInt();
        Serial.print( F("Adding time to the durationRemaining; duration: ") );
        Serial.println( duration );
        
        if( duration == -1 ) { 
          durationRemaining = -1;
        } else {
          durationRemaining += duration;
        }
    } else if( command == 2 ) {
        durationRemaining = 0;
    } else {
        Serial.print( F("Unexpected command; command: ") );
        Serial.println( command );
    }
}
