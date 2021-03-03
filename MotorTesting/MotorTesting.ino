 int pvmPin = 9; 
int PWMLOW = 1100; 
int PWMHigh = 1900;

int old = 1600; 
int PWMVAL = 1600; 

void setup() {
  pinMode(pvmPin, OUTPUT); 
  Serial.begin(9600); 
  analogWrite(pvmPin,old); 
}

void loop() {
  /*for(int x = PWMLOW; x < PWMHigh; x += 10) { 
    analogWrite(pvmPin,x); 
    delay(100); 
    Serial.println(x); 
  }*/
  if (Serial.available()) {
    String msgCurr = "";
    char chrIn = Serial.read();
    msg += chrIn; 
    PWMVAL = msg.toInt();
    if(PWMVAL != old) { 
       analogWrite(pvmPin, PWMVAL); 
       Serial.println("Send a pwm value of " + PWMVAL); 
       old = PWMVAL; 
    }
    delay(50); 
  }
}
