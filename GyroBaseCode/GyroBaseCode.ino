/*
    MPU6050 Triple Axis Gyroscope & Accelerometer. Pitch & Roll Accelerometer Example.
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-zyroskop-i-akcelerometr-mpu6050.html
    GIT: https://github.com/jarzebski/Arduino-MPU6050
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include <MPU6050.h>
unsigned long timer = 0;
float waitTime = 0.1; 
int last[] = {0, 0};
int bound = 5;
MPU6050 mpu;

void setup() 
{
  Serial.begin(115200);

  //Serial.println("Initialize MPU6050");

  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

  timer = millis();
}

void loop()
{
  if((millis() - timer) >= 1000 * waitTime) { 
    Vector normAccel = mpu.readNormalizeAccel();
  
    // Calculate Pitch & Roll
    int pitch = -(atan2(normAccel.XAxis, sqrt(normAccel.YAxis*normAccel.YAxis + normAccel.ZAxis*normAccel.ZAxis))*180.0)/M_PI;
    int roll = (atan2(normAccel.YAxis, normAccel.ZAxis)*180.0)/M_PI;
    if(abs(last[0] - pitch) > bound || abs(last[1] - roll) > bound) { 
      // Output
      Serial.print(pitch);
      Serial.print(",");
      Serial.println(roll);  
      last[0] = pitch; 
      last[1] = roll;
    }
    timer = millis();
  }
}
