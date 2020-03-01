#include <Wire.h>;
#include <Adafruit_PWMServoDriver.h>;
#include <Servo.h>;
int num_motor = 6; 
int num_claws = 2; 
int pwm_values[] = {9, 8, 7, 6, 5, 4, 3, 2}; //Last num_claws values are for claws (currently the last 2)
int motor_values[num_motor + num_claws]; 
boolean updated[num_motor + num_claws]; 
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(9600); 
  for(int i = 0; i < num_motor; i++) { 
    Servo ser; 
    ser.attach(pwm_values[i]); 
    ser.writeMicroseconds(1500); 
    servos[i] = ser; 
    motor_values[i] = 1500; 
  } 
  pwm.begin();
  pwm.setPWMFreq(60);
  Wire.setClock(100000);
  delay(5000);
}

void loop() {
  if(Serial.avaliable()) { 
    read_values(); 
    String s = ""; 
    for(int  i = 0; i < num_claw + num_motor; i++) { 
      if(updated[i]) { 
        s += String(motor_values[i]) + " ";
      } else { 
        s += "NU "; 
      }
    }
    Serial.println(s); 
  } 
  for(int i = 0; i < num_motors + num_claws; i++) { 
    if(updated[i]) { 
      pwm.setPWM(pwm_values[i], 0, motor_values[i]); 
      updated[i + num_motors] = false; 
    }
  }
}

void read_values(){ 
  String msg = Serial.readString();
  int index = msg.indexOf(";"); 
  if(index > -1) { 
    msg = msg.substring(0, index);
    index = 0; 
    while(msg.length() > 0 and index < pwm_values.length()) { 
      endindex = 0; 
      while(endindex < msg.length() && msg.charAt(endindex) != ",") { 
        endindex += 1; 
      }
      int new_number = msg.substring(0, endindex).toInt(); 
      updated[index] = new_number != motor_values[index];
      motor_values[index] = new_number;  
      msg.substring(endindex + 1); 
      index += 1;
    }
  }
}
