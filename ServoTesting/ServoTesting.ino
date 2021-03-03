#include <Servo.h>; 

int old = 1500; 
int PWMVAL = 1500; 
int scale = 0; 
int rate = 5; 
int stopval = 50; 
Servo servo1;

void setup() {
 servo1.attach(9); 
 Serial.begin(9600); 
 servo1.writeMicroseconds(old); 
 delay(5000);
}

void read_line() { 
  String msg = Serial.readString();
  int index = msg.indexOf(";"); 
  if(index > -1) { 
    msg = msg.substring(0, index);
    old = PWMVAL;
    PWMVAL = msg.toInt();
    scale = PWMVAL - old; 
  }
  
}

void loop() {
  if (Serial.available()) { 
       read_line(); 
       int theta = 0;
       while(theta <= 90) { 
          servo1.writeMicroseconds((int) (old + scale * sin(theta * PI/180))); 
          if(Serial.available()) { 
            read_line();
            theta = 0;    
          }
          theta += rate;
          delay(stopval); 
       }
    }
}
