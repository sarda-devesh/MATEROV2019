#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS A0
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int dirPin[] = {12, 13, 4, 2, 8, 7};
int s = 6;
int claw = 1;
int pvmPin[] = {10, 11, 5, 3, 9, 6, 15, 3};
int val[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int lastVal[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
String msg = "";
int water = A1;
int wcount = 0;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int SERVOMIN = 140; 
int SERVOMAX = 500;
double average = (SERVOMIN + SERVOMAX) / 2.0;
double spread = (SERVOMAX - SERVOMIN) / (2.0 * 105);
int count = 5;

float currenttemp = 0.0;

void setup() {
  Serial.begin(9600);
  for (int x = 0; x < s; x++) {
    pinMode(dirPin[x], OUTPUT);
  }
  for (int x = 0; x < s; x++) {
    pinMode(pvmPin[x], OUTPUT);
  }
  pinMode(water,INPUT);
  pwm.begin();
  pwm.setPWMFreq(60);
  Wire.setClock(100000);
  sensors.begin();
}

void loop() {
  if (Serial.available()) {
    process();
  }
  for (int i = 0; i < s + claw; i++) {
    if (val[i] == lastVal[i]) {
      continue;
    }
    if (i >= s) {
      uint16_t claw = (uint16_t) (average + spread * (-1.0 * val[i]));
      pwm.setPWM(pvmPin[i], 0, claw);
      lastVal[i] = val[i];
    } else {
      int pvr = val[i];
      digitalWrite(dirPin[i], (pvr > 0) ? HIGH : LOW);
      analogWrite(pvmPin[i], abs(pvr));
      lastVal[i] = val[i];
    }
  }
  if(val[claw + s] == 1 && count >= 0) {
    sensors.requestTemperatures();
    currenttemp = sensors.getTempCByIndex(0);
    Serial.println(currenttemp);
    count -= 1;
  }
  if(count < 0) { 
    count = 5; 
    val[claw + s] = 0;
  }
  int value = analogRead(water);
  if(value > 1000) { 
    wcount++;
  } else { 
    wcount = 0;
  }
  if(wcount >= 5) { 
    Serial.println("Water inside pressure chamber");
    wcount = 0;
  }
}

void process() {
  String msgCurr = "";
  char chrIn = Serial.read();
  msg += chrIn;
  if (msg.indexOf(";") > 0) {
    msgCurr = msg.substring(0, msg.indexOf(";"));
    msg = msg.substring(msg.indexOf(";") + 3);
  }
  if (msgCurr != "") {
    int i = 0;
    while (msgCurr.indexOf(",") != -1) {
      val[i++] = msgCurr.substring(0, msgCurr.indexOf(",")).toInt();
      msgCurr = msgCurr.substring(msgCurr.indexOf(",") + 1);
    }
    val[i++] = msgCurr.substring(0, msgCurr.indexOf(";")).toInt();
  }
}
